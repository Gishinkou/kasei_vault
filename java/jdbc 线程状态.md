你这个问题其实已经进入**“数据库连接语义层”**了——这正是你做 DAL / 中间件时最核心、最容易踩坑的部分。

我帮你做一个**工程化分层总结**，把“所有需要关注的状态”按影响范围拆清楚，并标出哪些是**必须治理**、哪些是**容易忽略但致命**。

---

# 一、先给你一个总框架（非常关键）

数据库连接上的状态，可以分成 4 大类：

### 1️⃣ 事务控制类（最核心）

- `autoCommit`
    
- 当前事务是否开启
    
- 是否有未提交 / 未回滚
    
- 锁持有情况
    

👉 **影响：数据正确性 + 死锁 + 脏数据**  
👉 **优先级：最高**

---

### 2️⃣ 隔离与一致性类

- `transactionIsolation`
    
- MVCC 可见性（隐含）
    
- 一致性读 / 当前读
    

👉 **影响：读到的数据版本、并发行为**  
👉 **优先级：极高**

---

### 3️⃣ 路由 / 执行语义类

- `readOnly`
    
- `schema / catalog`
    
- SQL hint / 路由变量
    
- session routing 标记
    

👉 **影响：请求打到哪个库（主/从/分片）**  
👉 **优先级：极高（在分库分表 / 中间件中）**

---

### 4️⃣ Session 环境类（最容易被忽略）

- `SET xxx`（各种 session 变量）
    
- `time_zone`
    
- `sql_mode`
    
- `names / charset`
    
- 用户变量（`@var`）
    
- 临时表
    
- prepared statement（server-side）
    

👉 **影响：SQL 行为、解析方式、甚至结果**  
👉 **优先级：中高（但隐蔽性最高）**

---

# 二、逐项拆解：你列的这些状态

我们一个个讲清楚：

---

## 1️⃣ autoCommit（必须重点盯）

```java
conn.setAutoCommit(false);
```

### 语义

- true：每条 SQL 自动提交
    
- false：进入“显式事务模式”
    

---

### 中间件必须保证：

✅ 归还连接前恢复为 `true`

否则会出现：

- 下一个请求跑在**上一个请求的事务里**
    
- 锁不释放
    
- binlog / redo 行为异常
    

---

### 常见坑（真实线上会炸的）

```java
conn.setAutoCommit(false);
ps.executeUpdate();
// 忘了 commit / rollback
conn.close(); // 回池
```

👉 下一个人拿到这个 connection：

- 仍然在事务里
    
- 可能继承锁
    
- 甚至 commit 别人的数据
    

---

## 👉 结论

👉 **autoCommit 是连接池必须 reset 的第一优先级**

---

## 2️⃣ 事务本身状态（比 autoCommit 更重要）

不仅仅是 autoCommit，还包括：

- 是否有未结束事务
    
- 是否持有锁
    
- 是否执行过写操作
    

---

### 中间件必须做：

👉 在连接归还时：

```text
如果 autoCommit = false 且事务未结束
    → 强制 rollback
```

---

### 为什么必须 rollback

因为：

- DB 不知道你“逻辑结束了”
    
- 连接复用会带着旧事务
    

---

### 注意一个细节（你这个方向会很关心）

👉 有些数据库：

- **事务结束 ≠ 锁释放（立即）**
    
- rollback 可能触发额外 IO / undo
    

👉 所以：

- 频繁错误事务会拖垮系统
    

---

## 3️⃣ transactionIsolation（非常隐蔽但致命）

```java
conn.setTransactionIsolation(Connection.TRANSACTION_SERIALIZABLE);
```

---

### 影响

- 可见性（读到什么数据）
    
- 锁粒度
    
- 并发性能
    

---

### 常见级别（以 MySQL 为例）：

- READ_UNCOMMITTED
    
- READ_COMMITTED
    
- REPEATABLE_READ（默认）
    
- SERIALIZABLE
    

---

### 中间件必须保证：

👉 归还连接前恢复默认隔离级别

否则：

#### 例子：

上一个请求：

```java
set isolation SERIALIZABLE
```

下一个请求：

👉 所有 select 都变成加锁读（严重性能问题）

---

## 👉 结论

👉 isolation 是**“慢性炸弹”型问题**

---

## 4️⃣ readOnly（经常被低估）

```java
conn.setReadOnly(true);
```

---

### 作用（不同 DB 不同）：

- 优化执行计划
    
- 标记只读事务
    
- **路由到从库（中间件常用）**
    

---

### 在中间件中的意义

很多中间件：

```text
readOnly = true  → 走从库
readOnly = false → 走主库
```

---

### 风险

如果残留：

👉 写请求可能被路由到从库 → 报错 / 数据不一致

---

## 👉 结论

👉 readOnly 是**路由级关键状态**

---

## 5️⃣ schema / catalog（多库场景致命）

```java
conn.setSchema("db_xxx");
```

---

### 作用

- 决定 SQL 在哪个数据库执行
    

---

### 风险

连接复用时：

👉 上一个请求切到了 `db_a`  
👉 下一个请求以为在 `db_b`

👉 实际写错库

---

### 特别危险的场景

- 分库分表
    
- 动态数据源
    
- Vitess / ShardingSphere / 自研 DAL
    

---

## 👉 结论

👉 schema 是**数据正确性级别风险**

---

## 6️⃣ session 变量（最隐蔽、最难治理）

这是你做中间件必须深入理解的。

---

### 常见类型

#### 1）系统变量

```sql
SET time_zone = '+08:00';
SET sql_mode = 'STRICT_TRANS_TABLES';
SET autocommit = 0;
```

---

#### 2）字符集

```sql
SET NAMES utf8mb4;
```

---

#### 3）用户变量

```sql
SET @trace_id = 'xxx';
```

---

#### 4）业务变量

```sql
SET role = 'admin';
SET tenant_id = 1001;
```

---

### 这些变量的特点：

👉 **完全绑定在 connection（session）上**

👉 连接复用 = 状态继承

---

### 中间件的难点

你无法轻易：

- 枚举所有变量
    
- 自动 reset
    

---

### 真实问题例子

#### 例1：sql_mode 残留

```sql
SET sql_mode = '';
```

👉 后续 SQL 行为变了（比如 group by 不严格）

---

#### 例2：time_zone 残留

👉 时间字段全部偏移

---

#### 例3：tenant_id 残留

👉 数据越权访问（严重事故）

---

## 👉 结论

👉 session 变量是**最大的不确定性来源**

---

# 三、你做中间件必须关注的“额外状态”

除了你列的，还有这些必须纳入模型：

---

## 7️⃣ 临时表（temporary table）

```sql
CREATE TEMPORARY TABLE tmp_xxx ...
```

特点：

- session 级
    
- 连接关闭才消失
    

---

风险：

👉 下一个请求可能“看到”这个表

---

## 8️⃣ 用户锁 / advisory lock

```sql
SELECT GET_LOCK('xxx', 10);
```

特点：

- session 级锁
    

---

风险：

👉 锁被继承 → 死锁 / 卡死

---

## 9️⃣ server-side prepared statement

MySQL：

```sql
PREPARE stmt FROM 'select ...';
```

或驱动自动创建

---

风险：

- 数量有限
    
- 连接复用导致句柄泄露
    

---

## 🔟 cursor / streaming result

未消费完 ResultSet：

👉 后续 SQL 失败（MySQL 很典型）

---

# 四、总结一张“必须治理清单”（中间件视角）

如果你在做 DAL / 连接池 / 中间件：

---

## ✅ 必须 reset（硬性）

- autoCommit
    
- 未结束事务 → rollback
    
- transactionIsolation
    
- readOnly
    
- schema/catalog
    

---

## ⚠️ 强烈建议治理

- session variables（尽量限制或检测）
    
- sql_mode / time_zone
    
- prepared statement cache
    
- fetchSize / timeout（statement级）
    

---

## ⚠️ 需要策略处理（无法完全自动）

- 临时表
    
- 用户变量（@xxx）
    
- advisory lock
    
- streaming result
    

---

# 五、一个中间件设计层面的关键思想

你可以把 Connection 分成：

## 👉 “纯净连接” vs “污染连接”

### 理想状态

```text
连接借出 → 使用 → 完全恢复 → 归还
```

---

### 实际问题

```text
连接借出 → 被污染（session变量/事务） → 归还 → 下一个请求踩雷
```

---

### 所以中间件常见策略：

#### 1️⃣ reset（重置）

- 尽可能恢复状态
    

#### 2️⃣ discard（丢弃）

- 检测到异常状态直接销毁连接
    

#### 3️⃣ forbid（禁止）

- 禁止执行某些 SQL（如 SET）
    

#### 4️⃣ proxy（代理）

- 拦截所有行为，维护虚拟状态
    

---

# 六、给你一个“工程判断口诀”

你以后判断一个 JDBC 状态是否危险，可以问：

👉 **这个状态是不是“session 级别的”？**

如果是：

👉 **那它一定会在连接复用时产生问题**

---

# 七、如果你往更深走（你这个方向很适合）

下一步你可以深入这些：

- MySQL session state reset 机制
    
- `COM_RESET_CONNECTION`（MySQL协议）
    
- Hikari / Druid reset 实现
    
- Vitess 如何隔离 session 状态
    
- Proxy 层如何虚拟 session（很关键）
    

---

如果你愿意，我可以下一步帮你画一个：

👉 **“JDBC Connection 在连接池 + 中间件中的完整生命周期 + 状态流转图（含 reset 点）”**

这个对你现在做 DAL 会非常有帮助。