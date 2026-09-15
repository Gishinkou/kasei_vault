可以把 JDBC 资源分成 4 层来看：

1. **驱动 / DataSource 层**
    
2. **Connection 层**
    
3. **Statement / PreparedStatement / CallableStatement 层**
    
4. **ResultSet 层**
    

如果你关心“复用、状态残留、并发安全”，核心其实是两句话：

- **最常被复用的是 Connection，其次可能是 PreparedStatement。**
    
- **越靠下层的对象，越不该跨线程共享，越容易出现状态残留。**
    

下面我按“对象职责 → 生命周期 → 复用 → 残留状态 → 并发安全”梳理。

---

## 1. 全景图：JDBC 一次调用大概发生什么

典型代码：

```java
Connection conn = dataSource.getConnection();
PreparedStatement ps = conn.prepareStatement(
    "select * from user where id = ?"
);
ps.setLong(1, 123L);
ResultSet rs = ps.executeQuery();
while (rs.next()) {
    // read
}
rs.close();
ps.close();
conn.close();
```

表面上看只有 3 个资源：

- `Connection`
    
- `PreparedStatement`
    
- `ResultSet`
    

但背后还包含：

- `Driver`
    
- `DataSource`
    
- 连接池中的物理连接 / 逻辑连接
    
- 数据库服务端游标、服务端 prepared statement、事务上下文、session 变量等
    

所以“close”也不一定真关闭，尤其在连接池场景下：

- `Connection.close()`：通常是**归还给池**
    
- `Statement.close()`：通常是真释放 statement 相关资源
    
- `ResultSet.close()`：释放结果集/游标资源
    

---

# 2. 各对象的职责与关系

## 2.1 Driver / DataSource

### Driver

JDBC 驱动实现者，比如 MySQL Connector/J。

职责：

- 解析 JDBC URL
    
- 建立数据库连接
    
- 实现 `Connection` / `Statement` / `ResultSet` 等接口
    

一般你业务代码不会直接碰它。

### DataSource

这是应用最常接触的入口。

职责：

- 提供 `getConnection()`
    
- 在实际项目里，往往还带连接池能力，比如 HikariCP、Druid、DBCP
    

它本身一般是：

- **可共享**
    
- **线程安全地被多个请求同时调用**
    

---

## 2.2 Connection

### 它是什么

代表一个数据库会话（session）/ 连接上下文。

它承载很多状态：

- autoCommit
    
- transaction isolation
    
- readOnly
    
- catalog / schema
    
- holdability
    
- network timeout
    
- client info
    
- 当前事务是否开启
    
- session 级变量
    
- 临时表、锁、游标、prepared statement 上下文等
    

### 它不是“纯粹的 socket”

它更像：

- Java 侧：一个 JDBC 连接对象
    
- DB 侧：一个 session
    

所以它最容易有**状态残留**问题。

---

## 2.3 Statement / PreparedStatement / CallableStatement

### Statement

执行普通 SQL 文本。

```java
Statement st = conn.createStatement();
st.execute("update t set x=1");
```

特点：

- 每次带完整 SQL 文本
    
- 易受 SQL 拼接问题影响
    
- 可执行任意 SQL
    

### PreparedStatement

预编译语句。

```java
PreparedStatement ps = conn.prepareStatement(
    "update t set name=? where id=?"
);
ps.setString(1, "A");
ps.setLong(2, 1L);
ps.executeUpdate();
```

特点：

- SQL 模板固定，参数可变
    
- 更安全
    
- 可能有客户端/服务端缓存
    
- 更容易涉及“复用”和“参数残留”
    

### CallableStatement

调用存储过程。

它本质上也是 statement 的一种，额外多了：

- IN/OUT 参数
    
- 过程调用语义
    

---

## 2.4 ResultSet

### 它是什么

SQL 执行后的结果游标。

特点：

- 持有当前行指针
    
- 可能依赖底层 statement 和 connection
    
- 一般是最短命的资源
    

它通常和 Statement 强绑定：

- 关闭 Statement，往往也会关闭其 ResultSet
    
- 一个 Statement 再次执行新 SQL，旧 ResultSet 往往失效
    

---

# 3. 生命周期：谁先创建，谁先释放

一般顺序：

```text
DataSource
  -> Connection
       -> Statement / PreparedStatement
            -> ResultSet
```

释放顺序反过来：

```text
ResultSet.close()
Statement.close()
Connection.close()
```

推荐永远用 `try-with-resources`：

```java
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement("select * from t where id=?")) {
    ps.setLong(1, 1L);
    try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) {
            // ...
        }
    }
}
```

这能显著减少泄露和状态污染。

---

# 4. 哪些资源会复用

这是重点。

## 4.1 Connection：**最常复用**

在连接池里，`getConnection()` 拿到的通常不是全新物理连接，而是池中一个现成连接的包装。

也就是说：

- 这次请求拿到的连接
    
- 很可能是上个请求刚用完归还的连接
    

因此必须关注：

- 事务状态是否恢复
    
- autoCommit 是否恢复
    
- readOnly 是否恢复
    
- isolation 是否恢复
    
- session 变量是否恢复
    

### 典型风险

上一个请求这样用：

```java
conn.setAutoCommit(false);
conn.setTransactionIsolation(Connection.TRANSACTION_SERIALIZABLE);
```

如果异常退出或框架没清理干净，这个连接回池后，下一个请求拿到它，就可能继承这些状态。

所以成熟连接池都会在归还前或借出时做 reset。

---

## 4.2 PreparedStatement：**有时复用**

复用分几种：

### a. 应用层不复用

最常见。每次都：

- `prepareStatement`
    
- 设置参数
    
- 执行
    
- close
    

### b. 驱动层缓存

某些驱动支持 statement cache，例如：

- 客户端缓存 prepared statement
    
- 服务端 prepared statement 复用
    

这时你代码看起来每次新建，底层可能已缓存。

### c. 连接池/中间件层缓存

有些池或中间件会做 PSCache。

注意：**PreparedStatement 通常是和 Connection 绑定的**。

不是全局可复用，而是：

- 同一个连接上
    
- 同一条 SQL 模板
    
- 可能复用对应 prepared statement
    

---

## 4.3 ResultSet：**通常不复用**

结果集是一次执行结果的游标视图，通常：

- 不跨调用复用
    
- 不跨线程复用
    
- 不回池复用
    

它生命周期很短。

---

# 5. 哪些状态会残留

这是最关键部分。

---

## 5.1 Connection 的状态残留

### 1）事务状态

最危险。

包括：

- `autoCommit=false`
    
- 事务未提交
    
- 未回滚
    
- 持有锁
    

如果连接直接回池，后续请求可能：

- 跑在前一个事务里
    
- 看见奇怪锁等待
    
- 意外提交前一个请求的数据
    

所以连接归还前应确保：

- 没有未结束事务
    
- 恢复 `autoCommit=true`
    
- 必要时 rollback
    

很多池会在 `close()` 返回池时处理。

---

### 2）隔离级别

```java
conn.setTransactionIsolation(...)
```

如果改成 SERIALIZABLE、READ_UNCOMMITTED 等，后一个请求若继承，会出现：

- 性能异常
    
- 并发语义异常
    
- 锁行为变化
    

---

### 3）只读标记

```java
conn.setReadOnly(true)
```

有些数据库/驱动会利用这个优化或路由。  
若没恢复，后续写请求可能失败或行为异常。

---

### 4）catalog / schema

```java
conn.setCatalog(...)
conn.setSchema(...)
```

尤其多库场景下，如果连接复用但 schema 没恢复，下一个请求可能跑到错误库。

---

### 5）session 变量

如 MySQL 常见：

```sql
SET NAMES utf8mb4;
SET time_zone = '+08:00';
SET sql_mode = ...;
SET autocommit = 0;
```

或者业务自定义：

```sql
SET @trace_id = 'xxx';
```

这些是**数据库 session 级别状态**，和 JDBC Connection 强绑定。  
如果连接复用，这些值也可能残留。

这类问题尤其隐蔽，因为 Java 侧看不出来。

---

### 6）临时表、用户变量、锁

例如：

- temporary table
    
- advisory lock
    
- session lock
    
- named lock
    

这些如果跟 session 绑定，也可能随着连接复用带来影响。

---

### 7）network timeout / client info / holdability

这些相对少见，但理论上也属于连接状态。

---

## 5.2 PreparedStatement 的状态残留

PreparedStatement 残留主要是**参数和执行选项**。

### 1）参数残留

```java
PreparedStatement ps = conn.prepareStatement(
    "insert into t(a,b) values(?,?)"
);
ps.setInt(1, 1);
ps.setString(2, "x");
ps.executeUpdate();

ps.setInt(1, 2);
// 如果忘了 setString(2, ...)
ps.executeUpdate();
```

第二次执行时，参数 2 可能仍是上一次的 `"x"`。

所以复用同一个 `PreparedStatement` 时，必须意识到：

- 参数是绑定在 statement 上的
    
- 不会自动“全部清空成未设置”
    

有 `clearParameters()`，但很多代码靠“每次全部重新 set 一遍”更稳。

---

### 2）批处理残留

```java
ps.addBatch();
```

如果没有适当清理，下一次可能继续带着旧 batch。

---

### 3）fetchSize / maxRows / queryTimeout / poolable 等选项

这些设置在 statement 上：

- `setFetchSize`
    
- `setMaxRows`
    
- `setQueryTimeout`
    
- `setFetchDirection`
    

如果 statement 被缓存复用，就可能污染下一次执行。

---

### 4）ResultSet 关闭联动

一个 Statement 通常只适合顺序使用。  
重复执行 SQL 可能会关闭前一个 ResultSet。

---

## 5.3 ResultSet 的状态残留

ResultSet 本身不太讲“残留后给别人用”，因为一般不会复用。

但它有几个典型问题：

### 1）游标位置状态

- 当前行指针在哪里
    
- 是否已经读完
    

### 2）流式读取未消费完

某些驱动/模式下，如果 ResultSet 没有完全读取或关闭，会影响后续语句执行。

MySQL 尤其要注意某些 streaming result 场景。

### 3）依赖上层对象

ResultSet 往往依赖其 Statement/Connection 存活。  
上层关闭后再读，可能报错。

---

# 6. 并发安全：哪些能共享，哪些别共享

结论先说：

- **DataSource：通常线程安全，可共享**
    
- **Connection：不要跨线程共享**
    
- **Statement / PreparedStatement：不要跨线程共享**
    
- **ResultSet：绝不要跨线程共享**
    

---

## 6.1 DataSource 一般可并发使用

这是设计目标。

多个线程同时：

```java
dataSource.getConnection()
```

一般没问题，连接池内部会做同步/并发控制。

---

## 6.2 Connection 通常不是线程安全对象

虽然有些驱动未必明确说“绝对不安全”，但实践中都应视为：

**单线程、单事务、单调用上下文使用。**

原因：

### 1）Connection 承载会话状态

一个线程改：

```java
conn.setAutoCommit(false);
```

另一个线程同时在这个 conn 上执行查询，会共享同一个事务上下文。

### 2）协议层通常不适合乱序共享

数据库连接通常对应一条 socket/协议会话。  
多个线程同时往同一连接发请求，驱动需要极强同步才能正确处理响应匹配。

### 3）事务边界会乱

线程 A 想提交自己的事务，线程 B 也在这个连接上跑 SQL，语义就混了。

所以一般原则：

**一个 Connection 在同一时刻只属于一个线程/请求。**

---

## 6.3 Statement / PreparedStatement 更不该跨线程共享

因为它们内部有大量可变状态：

- 当前 SQL / 编译状态
    
- 参数绑定
    
- batch 内容
    
- 当前 ResultSet
    
- timeout/fetchSize 等配置
    

两个线程共享一个 `PreparedStatement`，几乎必出事：

```java
Thread A: ps.setInt(1, 100)
Thread B: ps.setInt(1, 200)
Thread A: ps.executeQuery()
```

A 执行时参数到底是 100 还是 200，完全不可靠。

---

## 6.4 ResultSet 完全不适合共享

它本质是可变游标：

- 一个线程 `next()`
    
- 另一个线程也 `next()`
    

结果顺序和读取位置马上混乱。

---

# 7. 在连接池场景下，最该关注什么

你做中间件或连接池相关工作时，最重要的是 **Connection 归还池前的清理**。

## 7.1 必须恢复的典型连接状态

常见至少包括：

- autoCommit
    
- readOnly
    
- transactionIsolation
    
- catalog / schema
    
- 未结束事务 -> rollback
    
- 警告信息清理
    
- session state reset（视驱动/数据库能力）
    

---

## 7.2 不好彻底恢复的状态

最麻烦的是数据库 session 内部状态：

- `SET xxx`
    
- 临时表
    
- user variable
    
- lock
    
- prepared statement server-side handle
    
- 某些 optimizer/session 开关
    

这些不是所有池都能完美重置。

有些数据库/驱动支持类似 reset session 的能力；  
没有的话，只能：

- 约束业务不要乱改 session 状态
    
- 或直接丢弃该连接，不放回池
    

---

## 7.3 连接池为什么喜欢代理 Connection

因为池返回给应用的通常不是物理连接本体，而是一个代理对象，目的是：

- 拦截 `close()`，改成“归还池”
    
- 记录借出时间
    
- 做 leak detection
    
- 做状态重置
    
- 禁止错误使用
    

这也是为什么 `conn.close()` 在池里通常不是真关闭。

---

# 8. 什么时候会考虑 Statement 级复用

通常只在以下场景认真考虑：

## 8.1 高频固定 SQL

同一连接反复执行同一模板 SQL，PreparedStatement 复用可能减少：

- SQL 解析成本
    
- 编译成本
    
- 对象创建成本
    

## 8.2 驱动支持 statement cache

例如一些驱动支持：

- cachePrepStmts
    
- prepStmtCacheSize
    
- useServerPrepStmts
    

这时需要关注：

- 缓存命中率
    
- 服务端 prepared statement 数量上限
    
- 参数/批次/执行选项残留
    
- 连接关闭后缓存生命周期
    

---

# 9. 实际编码时最稳妥的原则

## 9.1 原则一：Connection 不跨线程传递

一个方法拿到连接，就在当前调用链/事务范围内使用。

不要：

- 放进单例字段
    
- 缓存到 map 里跨请求复用
    
- 多线程共用一个 conn
    

---

## 9.2 原则二：Statement 不跨方法长期保存

除非你非常清楚自己在做 statement cache，否则不要把：

- `Statement`
    
- `PreparedStatement`
    

存成成员变量长期复用。

最稳做法是“按次创建，按次关闭”。

---

## 9.3 原则三：每次完整设置 PreparedStatement 参数

不要依赖上次残留值。

```java
ps.setXxx(1, ...)
ps.setXxx(2, ...)
ps.setXxx(3, ...)
```

每次都完整设置。

---

## 9.4 原则四：任何 ResultSet 都尽快关闭

尤其大结果集、流式读取、长事务场景。

---

## 9.5 原则五：改过 Connection 状态就要恢复

比如：

```java
boolean oldAutoCommit = conn.getAutoCommit();
try {
    conn.setAutoCommit(false);
    ...
    conn.commit();
} catch (Exception e) {
    conn.rollback();
    throw e;
} finally {
    conn.setAutoCommit(oldAutoCommit);
}
```

如果在 Spring 事务、连接池代理下，框架通常会帮你处理一部分，但中间件开发者不能想当然。

---

# 10. 一个资源视角的“危险排行”

按最容易出问题排序，大概是：

## 第一名：Connection 状态残留

因为它会跨请求复用，还带 session 语义。

最常见坑：

- 上个事务没收尾
    
- autoCommit/readOnly/isolation 残留
    
- session variable 残留
    

## 第二名：PreparedStatement 参数残留

尤其手工缓存/复用 PS 时。

最常见坑：

- 少设一个参数，沿用旧值
    
- batch 没清
    
- queryTimeout/fetchSize 被污染
    

## 第三名：ResultSet 未关闭

导致：

- 资源泄露
    
- 游标占用
    
- 后续语句异常
    
- 连接迟迟不能安全归还
    

## 第四名：跨线程共享连接或 statement

这是设计层面的错误，后果很随机，也最难排查。

---

# 11. 一张简表

|对象|典型是否复用|主要残留状态|线程安全建议|
|---|---|---|---|
|DataSource|会，被全局共享|基本不谈“残留”|通常线程安全|
|Connection|会，被连接池复用|事务、autoCommit、readOnly、isolation、schema、session变量|不要跨线程共享|
|Statement|一般不复用|maxRows、fetchSize、timeout、当前结果集|不要跨线程共享|
|PreparedStatement|有时复用/缓存|参数、batch、执行选项、服务端句柄|不要跨线程共享|
|ResultSet|基本不复用|游标位置、流读取状态|绝不要跨线程共享|

---

# 12. 你可以把 JDBC 理解成两类资源

## 一类：**会话资源**

核心是 `Connection`

特点：

- 最贵
    
- 最可能复用
    
- 最容易状态污染
    
- 最值得连接池重点治理
    

## 一类：**执行资源**

核心是 `Statement / PreparedStatement / ResultSet`

特点：

- 生命周期更短
    
- 跟某次 SQL 执行强绑定
    
- 不应跨线程
    
- 更容易因“缓存优化”引入参数残留问题
    

---

# 13. 一个很实用的心智模型

你可以这样理解：

- `Connection` = “这次进数据库的身份和房间”
    
- `PreparedStatement` = “房间里的一张可重复填写的表单”
    
- `ResultSet` = “这次查出来的一摞纸”
    

于是：

- 房间会被下个人继续用，所以要打扫干净
    
- 表单复用时，上次填的内容可能还在
    
- 那摞纸看完就该收走，不能几个人一起乱翻
    

---

如果你愿意，我下一条可以继续给你整理成更偏工程实战的版本，比如：

**“连接池 / Spring 事务 / MyBatis 场景下，JDBC 这些资源分别是谁创建、谁关闭、谁 reset、谁最容易出 bug。”**