## 项目模块

Sentinel 具有清晰的模块分层，并在上层对大量开源框架进行适配。

## 核心概念

### 资源ID（ResourceKey）

**从哪来？**：`ResourceKey`通常是业务研发自己拼的一个字符串，标识进程级别的限流最小单位。在DongDAL 埋点中，一个物理库是一个资源 ID。所有访问同一个库的数据库连接池共享同一个资源ID。

`ResourceKey` 是我们关注的最小单元，一个资源ID也就对应了一个令牌桶，一个进程内不管并发量多大，都是对这同一个资源ID的操作。

这个过程可以画一张图，所有资源的入口

```
流量 --> SphU.entry(resourceKey) --> entry.exit()
```

### 调用链路（DefaultNode) （NodeSelectorSlot）

Sentinel 的文档中提到，DefaultNode 是 “资源 + 调用路径” 维度的节点，与此同时，还有 EntranceNode1 等入口、中途节点。
```plain
Context (ThreadLocal)  
└── curEntry（当前节点指针）
```
该模型可以理解为，是一个**线程级的调用链（像栈）指针**，最终可以形成这样的结构。

```plain
machine-root
   ├── EntranceNode1
   │       └── DefaultNode(nodeA)
   │              └── DefaultNode(nodeB)
   │
   └── EntranceNode2
           └── DefaultNode(nodeA)
```

调用链数据结构本质上是一个`无头结点的链表（尾插法）`

创建入口的动作，来自`ContextUtil.enter("entrance1");`，主要语义是开辟一个新的线程变量，作为链的头结点。因此这里的用词是`ContextUtil`。此时主要做了`创建 ThreadLocal`并`把头结点标记为null，此时还没有任何调用链路。

负责创建节点的模块叫`NodeSelectorSlot`，第一次 `entry()` 的动作，由于是**无头结点的尾插链表**，因此新建出来的节点成为头结点，而线程级的`current`指针其实就是链表尾指针。


> 头结点这个概念，在英文数据结构教材中，叫作 `sentinel node`，和 alibaba Sentinel 产品命名撞上了


## 资源节点（ClusterNode）ClusterBuilderSlot

上文我们提到了**资源（Resource）**与资源ID**（ResourceKey）**，本章节讲解资源的整合方式。

资源 ID 的存在实体是`ClusterNode`


### 多 caller 情况（多origin）

`caller`本质是一个额外的 tag，会导致同一个`Resource`的**分桶统计**

`caller` tag 的启用方式，是在 `ContextUtil.enter(...)` 方法调用时显式地传入。

```
ContextUtil.enter("entrance1", "caller1");
```
这里的`"caller1"`是 origin （调用来源）

```plain
ClusterNode(nodeA)
   ├── origin: caller1
   ├── origin: caller2
```

```
                    请求
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   Context        resourceId      origin
 (入口/链路)       (资源)         (调用方)
        │             │             │
        ▼             ▼             ▼
  NodeSelector   ClusterNode   origin stats
     构建树         全局统计       分桶统计
```

剧透一下：每个 `ClusterNode`和 `origin`是独立的**计算桶**，都会独立分配一套qps窗口统计器。这个**计算桶**的实体是`StatisticNode`。`ClusterNode`和`origin`都继承自这个类，因此各自具有独立的计算桶资源。

### `StatisticNode`——**计算桶**

一个请求进来，我们需要同时更新多个不同维度的计算桶，来获取不同维度上的统计结果。如我们同时有一个全局统计和两个分桶统计，则这里会用到`1+2`三个计算桶，一个 quest 会触发这三个桶的计数更新。

Sentinel 的指标系统使用滑动窗口算法收集受保护资源的实时统计信息。该系统维护两种时间粒度：二级指标用于即时流量控制决策，分钟级指标用于监控和历史分析。所有指标都存储在`StatisticNode`实例中，这些实例聚合了来自并发请求的数据，并采用**无锁原子操作**。

### 架构概述

该指标系统采用`LeapArray`滑动窗口和循环数组桶作为其核心数据结构。每个受保护的资源都有一个`StatisticNode`维护两个独立`ArrayMetric`实例的机制，分别封装`LeapArray`不同时间尺度的独立结构。


### LeapArray： 循环数组滑动窗口算法

分析一下我们的需求：维护一个**固定的观测窗口**，根据观测窗口内的总计数（除以秒数就是qps）或成功率（成功计数/总计数）来触发qps限流或成功率熔断。

### 为什么不直接用 `Map<timestamp, bucket>`
表面看，Map 很自然：
```java
Map<Long, Bucket> buckets;
```

key 是时间片起点，比如：
```
12:00:00.000 -> bucketA  
12:00:00.500 -> bucketB
```

好像很好理解。但工程上会有几个问题。
- 问题一：时间片是连续流动的，Map 会不断创建新 key
	- 旧 key必须删除，新 key必须创建
	- 有持续的对象抖动（churn）
- 问题二：