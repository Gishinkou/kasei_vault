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

### 调用链路（DefaultNode)

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



