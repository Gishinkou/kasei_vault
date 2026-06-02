下面给你一份**Java 后端面试复习提纲**，按“高频程度 + 深度要求”组织。你可以把它当成 checklist 来刷。

## 1. Java 基础语法与面向对象

### 必掌握

- 基本类型、包装类型、自动装箱/拆箱
    
- `==` 和 `equals`
    
- `hashCode` 和 `equals` 的关系
    
- `String`、`StringBuilder`、`StringBuffer`
    
- `final`、`static`、`abstract`、`interface`
    
- 重载 overload 和重写 override
    
- 访问修饰符：`private`、默认、`protected`、`public`
    
- 深拷贝、浅拷贝
    
- Java 值传递机制
    

### 高频问题

- Java 是值传递还是引用传递？
    
- `String s = new String("abc")` 创建几个对象？
    
- `final` 修饰变量、方法、类分别是什么意思？
    
- 抽象类和接口有什么区别？
    
- 为什么重写 `equals` 必须重写 `hashCode`？
    

---

## 2. 集合框架

### List

- `ArrayList`
    
- `LinkedList`
    
- `Vector`
    
- `CopyOnWriteArrayList`
    

重点：

- `ArrayList` 底层数组扩容机制
    
- `ArrayList` 和 `LinkedList` 区别
    
- `ArrayList` 删除元素的复杂度
    
- `Arrays.asList()` 返回什么
    
- fail-fast 和 fail-safe
    

### Map

- `HashMap`
    
- `LinkedHashMap`
    
- `TreeMap`
    
- `ConcurrentHashMap`
    
- `Hashtable`
    

重点：

- `HashMap` 底层结构：数组 + 链表 + 红黑树
    
- `put` 流程
    
- 扩容机制
    
- 哈希冲突解决
    
- 为什么容量通常是 2 的幂
    
- JDK 1.7 和 JDK 1.8 HashMap 区别
    
- `HashMap` 为什么线程不安全
    
- `ConcurrentHashMap` 如何保证线程安全
    

### Set

- `HashSet`
    
- `LinkedHashSet`
    
- `TreeSet`
    

重点：

- `HashSet` 底层其实是 `HashMap`
    
- `TreeSet` 排序依赖 `Comparable` / `Comparator`
    

---

## 3. Java 异常体系

### 必掌握

- `Throwable`
    
- `Error`
    
- `Exception`
    
- checked exception
    
- unchecked exception
    
- `RuntimeException`
    

### 高频问题

- checked exception 和 unchecked exception 区别
    
- `try-catch-finally` 执行顺序
    
- `finally` 一定会执行吗？
    
- `return` 和 `finally` 同时存在时怎么执行？
    
- 自定义异常怎么设计？
    

---

## 4. 泛型、反射、注解

### 泛型

- 泛型擦除
    
- 通配符 `? extends T` / `? super T`
    
- 泛型方法
    
- 泛型类
    
- 泛型数组为什么不推荐
    

高频问题：

- Java 泛型是真泛型还是伪泛型？
    
- 什么是类型擦除？
    
- `List<String>` 和 `List<Integer>` 运行时是同一个类型吗？
    
- `extends` 和 `super` 怎么理解？
    

### 反射

- `Class`
    
- `Method`
    
- `Field`
    
- `Constructor`
    
- 动态创建对象
    
- 调用方法
    
- 修改访问权限
    

高频问题：

- 反射为什么慢？
    
- 反射破坏了什么？
    
- Spring 为什么大量使用反射？
    

### 注解

- 元注解：`@Target`、`@Retention`、`@Documented`、`@Inherited`
    
- 编译期注解
    
- 运行期注解
    
- 注解和反射的配合
    

---

## 5. JVM

这是 Java 面试的核心。

## 5.1 JVM 内存结构

必须掌握：

- 程序计数器
    
- Java 虚拟机栈
    
- 本地方法栈
    
- 堆
    
- 方法区 / 元空间
    
- 运行时常量池
    
- 直接内存
    

高频问题：

- 堆和栈的区别？
    
- 对象一定分配在堆上吗？
    
- 方法区和永久代、元空间的关系？
    
- `String.intern()` 怎么理解？
    
- 栈溢出和堆溢出分别怎么产生？
    

---

## 5.2 对象创建与内存布局

重点：

- 类加载检查
    
- 分配内存
    
- 初始化零值
    
- 设置对象头
    
- 执行构造方法
    

对象内存布局：

- 对象头
    
- 实例数据
    
- 对齐填充
    

高频问题：

- `new Object()` 过程是什么？
    
- 对象头里有什么？
    
- 对象怎么定位？
    
- 指针压缩是什么？
    

---

## 5.3 类加载机制

必须掌握：

- 加载 Loading
    
- 验证 Verification
    
- 准备 Preparation
    
- 解析 Resolution
    
- 初始化 Initialization
    

类加载器：

- Bootstrap ClassLoader
    
- Extension / Platform ClassLoader
    
- Application ClassLoader
    
- 自定义 ClassLoader
    

重点：

- 双亲委派模型
    
- 打破双亲委派的场景
    
- SPI
    
- Tomcat 类加载机制
    

高频问题：

- 什么是双亲委派？
    
- 为什么要双亲委派？
    
- 哪些场景会打破双亲委派？
    
- 类什么时候会初始化？
    

---

## 5.4 GC 垃圾回收

必须掌握：

- 引用计数法
    
- 可达性分析
    
- GC Roots
    
- 强引用、软引用、弱引用、虚引用
    
- Minor GC
    
- Major GC
    
- Full GC
    

垃圾回收算法：

- 标记-清除
    
- 标记-复制
    
- 标记-整理
    
- 分代收集
    

垃圾收集器：

- Serial
    
- ParNew
    
- Parallel Scavenge
    
- CMS
    
- G1
    
- ZGC
    
- Shenandoah
    

高频问题：

- 对象什么时候会被回收？
    
- 哪些对象可以作为 GC Roots？
    
- Minor GC 和 Full GC 区别？
    
- CMS 和 G1 区别？
    
- G1 为什么适合大堆？
    
- 如何排查频繁 Full GC？
    
- 内存泄漏和内存溢出区别？
    

---

## 5.5 JVM 调优与排查

工具：

- `jps`
    
- `jstat`
    
- `jmap`
    
- `jstack`
    
- `jcmd`
    
- `arthas`
    
- VisualVM
    
- MAT
    
- async-profiler
    

必会场景：

- CPU 飙高
    
- 内存泄漏
    
- 频繁 Full GC
    
- 线程死锁
    
- 接口 RT 抖动
    
- OOM 分析
    
- 线程池堆积
    

高频问题：

- 线上 CPU 100% 怎么排查？
    
- 线上 OOM 怎么排查？
    
- 如何定位死锁？
    
- 如何分析 GC 日志？
    
- 如何导出 heap dump？
    
- 如何看某个线程在干什么？
    

---

## 6. Java 并发

这是面试重点中的重点。

## 6.1 线程基础

必须掌握：

- 线程生命周期
    
- `start()` 和 `run()`
    
- `sleep()`、`wait()`、`join()`、`yield()`
    
- 守护线程
    
- 线程中断 interrupt
    

高频问题：

- `sleep` 和 `wait` 区别？
    
- `start` 和 `run` 区别？
    
- 如何优雅停止一个线程？
    
- `interrupt` 是强制停止线程吗？
    

---

## 6.2 synchronized

必须掌握：

- 对象锁
    
- 类锁
    
- 锁对象
    
- 可重入性
    
- monitor
    
- 字节码层面：`monitorenter` / `monitorexit`
    
- 锁升级
    

锁状态：

- 无锁
    
- 偏向锁，较新 JDK 已逐渐弱化/废弃
    
- 轻量级锁
    
- 重量级锁
    

高频问题：

- `synchronized` 锁的是什么？
    
- 修饰普通方法和静态方法有什么区别？
    
- 为什么是可重入锁？
    
- 锁升级过程？
    
- `synchronized` 和 `ReentrantLock` 区别？
    

---

## 6.3 volatile

必须掌握：

- 可见性
    
- 有序性
    
- 不保证原子性
    
- 内存屏障
    
- happens-before
    

高频问题：

- `volatile` 能保证线程安全吗？
    
- `volatile int i++` 安全吗？
    
- DCL 单例为什么要加 `volatile`？
    
- `volatile` 和 `synchronized` 区别？
    

---

## 6.4 JMM Java 内存模型

必须掌握：

- 主内存
    
- 工作内存
    
- happens-before
    
- 指令重排序
    
- 内存屏障
    
- 可见性、原子性、有序性
    

高频问题：

- 什么是 JMM？
    
- 什么是 happens-before？
    
- 为什么会发生指令重排序？
    
- 如何禁止重排序？
    

---

## 6.5 JUC 并发包

重点类：

- `ReentrantLock`
    
- `ReadWriteLock`
    
- `StampedLock`
    
- `CountDownLatch`
    
- `CyclicBarrier`
    
- `Semaphore`
    
- `ThreadLocal`
    
- `AtomicInteger`
    
- `LongAdder`
    
- `BlockingQueue`
    
- `ConcurrentHashMap`
    

高频问题：

- `ReentrantLock` 和 `synchronized` 区别？
    
- 公平锁和非公平锁区别？
    
- AQS 是什么？
    
- `CountDownLatch` 和 `CyclicBarrier` 区别？
    
- `Semaphore` 使用场景？
    
- `ThreadLocal` 原理和内存泄漏问题？
    
- `AtomicInteger` 底层怎么实现？
    
- CAS 有什么问题？
    
- ABA 问题如何解决？
    
- `LongAdder` 为什么高并发下更快？
    

---

## 6.6 线程池

必须掌握：

- `ThreadPoolExecutor`
    
- 核心线程数
    
- 最大线程数
    
- 阻塞队列
    
- 拒绝策略
    
- 线程工厂
    
- keepAliveTime
    

执行流程：

1. 小于核心线程数，创建核心线程
    
2. 核心线程满了，进队列
    
3. 队列满了，创建非核心线程
    
4. 线程数达到最大值，执行拒绝策略
    

高频问题：

- 线程池参数有哪些？
    
- 线程池执行流程？
    
- 常见阻塞队列有哪些？
    
- 拒绝策略有哪些？
    
- 为什么不推荐 `Executors` 创建线程池？
    
- 线程池大小怎么设置？
    
- 线程池任务堆积怎么排查？
    
- 如何优雅关闭线程池？
    

---

## 7. IO 与网络编程

### IO 模型

必须掌握：

- BIO
    
- NIO
    
- AIO
    
- 阻塞 / 非阻塞
    
- 同步 / 异步
    
- select / poll / epoll
    

高频问题：

- BIO、NIO、AIO 区别？
    
- Java NIO 三大组件：Buffer、Channel、Selector
    
- 零拷贝是什么？
    
- mmap 是什么？
    
- Netty 为什么性能高？
    

---

## 8. Spring

## 8.1 Spring 基础

必须掌握：

- IOC
    
- DI
    
- AOP
    
- Bean 生命周期
    
- Bean 作用域
    
- 循环依赖
    
- 自动装配
    

高频问题：

- Spring IOC 是什么？
    
- Bean 生命周期？
    
- Spring 如何解决循环依赖？
    
- 三级缓存是什么？
    
- 哪些循环依赖解决不了？
    
- `@Autowired` 和 `@Resource` 区别？
    
- BeanFactory 和 ApplicationContext 区别？
    

---

## 8.2 Spring AOP

必须掌握：

- 代理模式
    
- JDK 动态代理
    
- CGLIB
    
- 切面 Aspect
    
- 切点 Pointcut
    
- 通知 Advice
    

高频问题：

- Spring AOP 原理？
    
- JDK 动态代理和 CGLIB 区别？
    
- 为什么同类内部方法调用 AOP 失效？
    
- `@Transactional` 为什么有时不生效？
    

---

## 8.3 Spring 事务

必须掌握：

- 事务传播行为
    
- 事务隔离级别
    
- rollback 规则
    
- 声明式事务
    
- 编程式事务
    

传播行为重点：

- `REQUIRED`
    
- `REQUIRES_NEW`
    
- `NESTED`
    
- `SUPPORTS`
    
- `NOT_SUPPORTED`
    
- `MANDATORY`
    
- `NEVER`
    

高频问题：

- Spring 事务传播行为有哪些？
    
- `REQUIRED` 和 `REQUIRES_NEW` 区别？
    
- 事务什么时候会失效？
    
- checked exception 会不会回滚？
    
- 自调用为什么事务失效？
    
- 事务和数据库连接是什么关系？
    
- Spring + MyBatis 下连接什么时候获取？
    

---

## 9. Spring Boot

必须掌握：

- 自动配置
    
- starter
    
- `@SpringBootApplication`
    
- 条件装配
    
- 配置绑定
    
- Actuator
    

高频问题：

- Spring Boot 自动配置原理？
    
- starter 是什么？
    
- `@SpringBootApplication` 包含哪些注解？
    
- `@ConditionalOnClass` / `@ConditionalOnMissingBean` 作用？
    
- Spring Boot 配置加载顺序？
    
- fat jar 是什么？
    
- Spring Boot jar 如何启动？
    

---

## 10. MyBatis

必须掌握：

- Mapper 代理
    
- SqlSession
    
- Executor
    
- StatementHandler
    
- ParameterHandler
    
- ResultSetHandler
    
- 一级缓存
    
- 二级缓存
    
- 插件机制
    

高频问题：

- MyBatis Mapper 接口为什么不用实现类？
    
- MyBatis 执行 SQL 流程？
    
- `#{}` 和 `${}` 区别？
    
- 一级缓存什么时候生效？
    
- 二级缓存有什么问题？
    
- MyBatis 插件原理？
    
- MyBatis 如何和 Spring 事务结合？
    

---

## 11. 数据库 MySQL

## 11.1 索引

必须掌握：

- B+ 树
    
- 聚簇索引
    
- 非聚簇索引
    
- 联合索引
    
- 最左前缀原则
    
- 覆盖索引
    
- 索引下推
    
- 回表
    
- 索引失效
    

高频问题：

- 为什么 MySQL 用 B+ 树？
    
- 聚簇索引和普通索引区别？
    
- 什么是回表？
    
- 什么是覆盖索引？
    
- 联合索引怎么设计？
    
- 哪些情况会导致索引失效？
    
- `like '%abc'` 为什么走不了索引？
    
- 索引是不是越多越好？
    

---

## 11.2 事务

必须掌握：

- ACID
    
- 隔离级别
    
- 脏读
    
- 不可重复读
    
- 幻读
    
- MVCC
    
- undo log
    
- redo log
    
- binlog
    
- 两阶段提交
    

高频问题：

- MySQL 默认隔离级别是什么？
    
- RC 和 RR 区别？
    
- MVCC 原理？
    
- 当前读和快照读区别？
    
- 幻读怎么解决？
    
- undo log 和 redo log 区别？
    
- binlog 和 redo log 区别？
    
- 为什么需要两阶段提交？
    

---

## 11.3 锁

必须掌握：

- 表锁
    
- 行锁
    
- 间隙锁
    
- next-key lock
    
- 共享锁
    
- 排他锁
    
- 意向锁
    
- 死锁
    

高频问题：

- InnoDB 行锁什么时候退化成表锁？
    
- 间隙锁是什么？
    
- next-key lock 是什么？
    
- 如何排查死锁？
    
- `select ... for update` 做了什么？
    
- update 没命中索引会怎样？
    

---

## 11.4 SQL 优化

必须掌握：

- `EXPLAIN`
    
- 慢 SQL
    
- 执行计划
    
- 索引选择性
    
- 分页优化
    
- join 优化
    
- 大表更新
    
- count 优化
    

高频问题：

- 一条 SQL 很慢怎么排查？
    
- `EXPLAIN` 重点看哪些字段？
    
- 深分页怎么优化？
    
- 大表加字段怎么做？
    
- 大批量更新怎么做？
    
- `count(*)`、`count(1)`、`count(column)` 区别？
    

---

## 12. Redis

必须掌握：

- String
    
- Hash
    
- List
    
- Set
    
- ZSet
    
- Bitmap
    
- HyperLogLog
    
- Stream
    
- GEO
    

高频问题：

- Redis 为什么快？
    
- Redis 单线程为什么还快？
    
- Redis 持久化 RDB / AOF 区别？
    
- Redis 过期删除策略？
    
- Redis 内存淘汰策略？
    
- 缓存穿透、击穿、雪崩怎么解决？
    
- 分布式锁怎么实现？
    
- Redisson 原理？
    
- Redis 主从、哨兵、集群区别？
    
- Redis Cluster 如何分片？
    
- 热 key、大 key 怎么处理？
    

---

## 13. 消息队列

常见：

- Kafka
    
- RocketMQ
    
- RabbitMQ
    

必须掌握：

- producer
    
- broker
    
- consumer
    
- topic
    
- partition
    
- consumer group
    
- offset
    
- ack
    
- 重试
    
- 死信队列
    
- 顺序消息
    
- 延迟消息
    
- 事务消息
    

Kafka 高频问题：

- Kafka 为什么吞吐高？
    
- partition 的作用？
    
- consumer group 怎么消费？
    
- offset 存在哪里？
    
- 如何保证消息不丢？
    
- 如何保证消息不重复消费？
    
- 如何保证顺序消费？
    
- 消息积压怎么排查？
    
- Kafka rebalance 是什么？
    
- ISR 是什么？
    
- acks 参数怎么设置？
    

---

## 14. 分布式系统

必须掌握：

- CAP
    
- BASE
    
- 一致性模型
    
- 分布式事务
    
- 幂等
    
- 限流
    
- 熔断
    
- 降级
    
- 超时
    
- 重试
    
- 服务注册发现
    
- 配置中心
    
- 负载均衡
    
- 链路追踪
    

高频问题：

- 什么是 CAP？
    
- 分布式事务有哪些方案？
    
- TCC、Saga、本地消息表、事务消息区别？
    
- 如何设计幂等？
    
- 接口重复请求怎么处理？
    
- 分布式锁有哪些实现？
    
- 如何做限流？
    
- 令牌桶和漏桶区别？
    
- 服务雪崩怎么处理？
    
- 如何做灰度发布？
    

---

## 15. 微服务与 RPC

必须掌握：

- HTTP
    
- REST
    
- RPC
    
- gRPC
    
- Dubbo
    
- Spring Cloud
    
- 注册中心
    
- 服务发现
    
- 负载均衡
    
- 超时重试
    
- 熔断降级
    

高频问题：

- HTTP 和 RPC 区别？
    
- Dubbo 调用流程？
    
- gRPC 为什么高效？
    
- 服务发现怎么做？
    
- 客户端负载均衡和服务端负载均衡区别？
    
- RPC 超时和重试怎么设计？
    
- 重试会带来什么问题？
    

---

## 16. 计算机网络

必须掌握：

- TCP 三次握手
    
- TCP 四次挥手
    
- TIME_WAIT
    
- CLOSE_WAIT
    
- 滑动窗口
    
- 拥塞控制
    
- 重传
    
- Nagle 算法
    
- HTTP/1.1
    
- HTTP/2
    
- HTTPS
    
- TLS
    

高频问题：

- 为什么三次握手？
    
- 为什么四次挥手？
    
- TIME_WAIT 为什么存在？
    
- CLOSE_WAIT 太多是什么原因？
    
- TCP 如何保证可靠？
    
- TCP 和 UDP 区别？
    
- HTTP 和 HTTPS 区别？
    
- HTTP/1.1 和 HTTP/2 区别？
    
- keep-alive 是什么？
    
- 连接池复用的是什么连接？
    

---

## 17. 操作系统与 Linux

必须掌握：

- 进程和线程
    
- 上下文切换
    
- 用户态和内核态
    
- 虚拟内存
    
- 文件描述符
    
- epoll
    
- page cache
    
- CPU load
    
- IO wait
    
- top / ps / netstat / ss / lsof / vmstat / iostat / sar
    

高频问题：

- 进程和线程区别？
    
- 什么是上下文切换？
    
- CPU 高怎么排查？
    
- load 高但 CPU 不高是什么情况？
    
- IO wait 高怎么排查？
    
- 文件描述符耗尽会怎样？
    
- `epoll` 为什么高效？
    

---

## 18. 设计模式

高频：

- 单例模式
    
- 工厂模式
    
- 策略模式
    
- 模板方法模式
    
- 代理模式
    
- 装饰器模式
    
- 观察者模式
    
- 责任链模式
    
- 建造者模式
    

面试重点不是背 UML，而是能说出：

- 解决什么问题
    
- 在 Spring / JDK / 项目哪里用过
    
- 优缺点
    
- 代码如何写
    

例子：

- Spring AOP：代理模式
    
- Spring Bean 创建：工厂模式
    
- `JdbcTemplate`：模板方法模式
    
- `Comparator`：策略模式
    
- Servlet Filter：责任链模式
    

---

## 19. 数据结构与算法

Java 面试至少要刷这些：

### 基础结构

- 数组
    
- 链表
    
- 栈
    
- 队列
    
- 哈希表
    
- 堆
    
- 二叉树
    
- 图
    
- Trie
    
- 并查集
    

### 高频算法

- 二分查找
    
- 双指针
    
- 滑动窗口
    
- 前缀和
    
- 单调栈
    
- 单调队列
    
- 回溯
    
- BFS
    
- DFS
    
- 动态规划
    
- 贪心
    
- 排序
    
- Top K
    
- LRU
    

### 高频题型

- 反转链表
    
- K 个一组反转链表
    
- 合并两个有序链表
    
- 环形链表
    
- LRU 缓存
    
- 最长无重复子串
    
- 最大子数组和
    
- 最小覆盖子串
    
- 滑动窗口最大值
    
- 接雨水
    
- 二叉树层序遍历
    
- 二叉树最近公共祖先
    
- 岛屿数量
    
- 合并区间
    
- topK 频率元素
    

---

## 20. 项目经验

这部分非常重要，尤其是社招。

你需要准备：

### 项目背景

- 项目解决什么业务问题
    
- 你的角色是什么
    
- 核心模块有哪些
    
- 技术栈是什么
    

### 技术难点

至少准备 2 到 3 个：

- 性能优化
    
- 慢 SQL 优化
    
- 缓存设计
    
- 并发问题
    
- 事务一致性
    
- 连接池优化
    
- 消息积压处理
    
- 大流量削峰
    
- 系统可用性提升
    

### 指标量化

尽量准备：

- QPS 提升多少
    
- RT 降低多少
    
- CPU / 内存下降多少
    
- 慢 SQL 从多少降到多少
    
- 错误率降低多少
    
- 成本下降多少
    

面试官喜欢听：

> 问题背景 → 原因分析 → 方案选择 → 落地细节 → 结果指标 → 复盘不足

---

# 推荐复习顺序

按优先级建议这样来：

1. **Java 基础 + 集合**
    
2. **JVM**
    
3. **并发 + 线程池**
    
4. **Spring / Spring Boot**
    
5. **MySQL**
    
6. **Redis**
    
7. **MQ**
    
8. **分布式系统**
    
9. **网络 + Linux**
    
10. **项目经验**
    
11. **算法题**
    

---

# 最小必会版

要是时间不多，先抓这些：

- `HashMap`
    
- `ConcurrentHashMap`
    
- `ArrayList`
    
- `synchronized`
    
- `volatile`
    
- `ThreadLocal`
    
- `ThreadPoolExecutor`
    
- AQS
    
- JVM 内存模型
    
- GC
    
- 类加载
    
- Spring IOC
    
- Spring AOP
    
- Spring 事务
    
- Spring Boot 自动配置
    
- MyBatis 执行流程
    
- MySQL 索引
    
- MySQL 事务 / MVCC
    
- Redis 缓存问题
    
- MQ 消息可靠性
    
- 分布式锁
    
- 幂等设计
    
- 限流熔断
    
- TCP / HTTP
    
- 项目性能优化案例
    

---

# 面试准备的核心标准

不要只背“是什么”，每个知识点最好能按这个结构讲：

```text
1. 它是什么
2. 为什么需要它
3. 底层怎么实现
4. 有什么优缺点
5. 常见坑是什么
6. 项目里怎么用过
7. 出问题怎么排查
```

比如 `ThreadLocal`，你要能讲：

```text
ThreadLocal 是线程本地变量。
每个 Thread 内部有一个 ThreadLocalMap。
key 是 ThreadLocal 弱引用，value 是实际对象。
如果线程池线程长期存活，value 可能无法释放。
所以用完要 remove。
常见应用是保存用户上下文、traceId、事务上下文。
```

这才是比较完整的面试回答。