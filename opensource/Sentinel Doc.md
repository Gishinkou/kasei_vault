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

Sentinel 的文档中提到，DefaultNode 是 “资源 + 调用路径” 维度的节点

调用链路是一个树结构