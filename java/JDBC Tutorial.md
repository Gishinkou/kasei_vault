文章约定：章节标题默认 2 级 sharp
## executeUpdate 还支持DDL

`executeUpdate`不止用于增删改 DML，还用于**建表**的DDL。

## Statement 的复用

注意以下情景，`Statement stmt`被复用，需要清除可能残留的状态。
```java
stmt.executeUpdate('INSERT INTO COFFEES VALUES ('italy', 49)');
stmt.executeUpdate('INSERT INTO COFFEES VALUES ('japan', 50)');
```

## ResultSet

```java
ResultSet rs = stmt.executeQuery("SELECT COF_NAME, PRICE FROM COFFEES");
```

| COF_NAME | PRICE |
|-----|----|
|Colombian|7.99|
|FrenchRost|8.99|
注意以上表行有几个元素：
1. 行 index
2. 列 名称
3. 列 index
4. 行列 的 value

### 处理行——cursor、迭代器next()

本阶段的处理对象是`ResultSet rs`，主要方法是`rs.next()`，固定写法是`while(rs.next())`

cursor (第一次调用后指向第一行 ，指向的叫做 currentRow，可以走向 nextRow)
搭配 while 使用，只要next方法为true，则本次 while 里必然可以稳定获得一行数据，并处理

### 处理列——(getInt, getString, getDouble)

避免思维短路：获取列值有按index获取和按列名获取的区别。这听起来理所当然，但是：
- 按index获取，我们需要知道index的range，这个拓展代价比较大；
- 相比之下按列名获取，本质是一个无序 Map，拓展只需额外维护一条键值对
#### 按列名`columnName`获取列值

本阶段的处理对象是`ResultSet rs`，且已经调用过`rs.next()`，主要处理各种行。
```java
List<Coffee> cofList = new ArrayList<>();
while (rs.next()) {
	String s = rs.getString("COF_NAME");
	float n = rs.getFloat("PRICE");
	Coffee cof = new Coffee(s, n);
	cofList.add(cof);
}
System.out.println("Great! I've go my coffees: " + cofList);
```

#### 按列 index 获取列值

```
rs.next();
String s = rs.getString(1);
float n = rs.getFloat(2);
```

### JDBCType 和 SqlTYPE是等价的

jdbcType 和`java.sql.Types`里的定义是完全等价的。


## PreparedStatement

主要区别：从“编译发生的地点”考虑：
- Statement：SQL立即发送，编译发生在**数据库**
- PreparedStatement：SQL已经**编译完成**，复用，但**编译发生在什么地方？**
### PreparedStatement 到底持有什么

- 有`?` 占位符
- 有 `setter` 绑定参数
- **数据库可以复用执行计划**

### 插播：数据库对一条SQL做哪些步骤
1. parseSQL: 语法层面的分析
2. optimize: SQL 优化
3. executionPlan：创建执行计划
4. return statement id：返回 `statement_id` （关键，这是后续传参数的凭据）
5. 客户端 `setInt/ setString` 等，设置参数
6. 客户端 `execute()`，将 `{参数 + statement_id}` 发出

### 关键问题： preparedStatement，编译发生在什么位置

从上述过程可以看出，`preparedStatement`主要是通过`prepareStatement(sql)`方法，理论上会**触发一次服务器编译**，并将 `statement_id`存在内存中，作为下次访问的凭据。

#### mysql 服务端的支持
但究竟是不是这样呢？让我们看一下 Mysql 文章中的 PrepareStatement 章节是怎么写的 [Mysql官方文档 15.5preparedStatements](https://dev.mysql.com/doc/refman/8.4/en/sql-prepared-statements.html)

>MySQL 8.4 provides support for server-side prepared statements. This support takes advantage of the efficient client/server binary protocol. Using prepared statements with placeholders for parameter values has the following benefits:
> - Less overhead for parsing the statement each time it is executed. Typically, database applications process large volumes of almost-identical statements, with only changes to literal or variable values in clauses such as `WHERE` for queries and deletes, `SET` for updates, and `VALUES` for inserts.
> - Protection against SQL injection attacks. The parameter values can contain unescaped SQL quote and delimiter characters.

文章中明确指出“server-side prepared statements”。这样做的好处有两点：1. 减少额外成本(overhead)，并且明确是"parsing statement"这种解析上的成本。2. 避免sql注入

但这仍是 server 端的策略，具体行为其实是一个client 和 server 端协同的过程，让我们看一下 jdbc-mysql 的实现。

#### jdbc-mysql 客户端驱动的实现

查看[mysql connectors documentation 6.4 jdbc api implementation notes](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html)，能看到mysql jdbc connector 的具体实现。

`PreparedStatement`章节入口就有一句：`Two variants of prepared statements are implemented by Connector/J, the client-side and the server-side prepared statements. `后续的具体内容为：

> Client-side prepared statements are used by default because early MySQL versions did not support the prepared statement feature or had problems with its implementation. Server-side prepared statements and binary-encoded result sets are used when the server supports them. To enable usage of server-side prepared statements, set `useServerPrepStmts=true`.

从上述文本，可以知道， mysql 默认采取 `client-side` 的编译，高版本的 mysql 即使支持 `server-side`编译，也需要显式地打开配置，set `useServerPrepStmts=true`。

因此，我们可以建立这样的心智模型： client 的 jdbc-mysql 默认带有 sql 编译能力，调用 `prepareStatement` 后，就能产生带有问号的语句，之后直接把该语句发送给 server，获取 `statement_id`，作为后续访问这个编译结果的凭据。

### PreparedStatement 如何执行

回到简单的 api 使用，我们理解了具体执行前，我们拿到了一个 statement token，有几个需要填入的参数。填完了以后，如何具体执行呢？

#### update 类型的执行
- `int executeUpdate()`：无参数，直接运行。
	- 不是`execute()`?
	- 返回值是一个 int，返回本次更新的行数
- 返回值为 0 的意义**有两种**：
	- `statement` DML 被执行了，且影响行数为 0
	- DDL 语句默认返回 0；

## 手搓事务

事务从**客户端**视角来看，就只有两件事：
1. 关闭**连接的自动提交机制**(`con.setAutoCommit(false);`)，然后在**关闭自动提交**的情况下，执行数条SQL语句
2. 提交事务（`con.commit();`）
3. 恢复自动提交 `con.setAutoCommit(true);`

事务是否开启，事务隔离等级，从客户端来看，是一个 setter，但在一个"client-server connection"资源的层级，是一个“会话状态“。

### 事务 setter 的工作实质——一条特殊 SQL

注意以下“驱动可能立马发送”可能并不准确，具体实现中可能延迟到第一条SQL、可能幂等不触发重复发送。这些也是连接池实现需要考虑的问题，连接池需要“重置”连接状态，但“重置”连接状态是一个需要网络IO的事情，需要优化避免无意义的 `no-op`通过网络发送过去。
```
conn.setAutoCommit(false);
驱动可能立马发送
SET autocommit=0;
```

```
conn.setTransactionIsolation(REPEATABLE_READ);
驱动可能立即发送
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```


### 尝试复原一下 Spring 事务管理在背后做的事情（主链路、简明）

1. 进入代理
2. 获取 `Connection`
3. 关掉 `autoCommit`
4. 把 `Connection` 绑定到当前线程
5. 执行业务里的 JDBC / MyBatis 代码
6. 成功就 `commit`
7. 失败就 `rollback`
8. 恢复连接状态并归还连接池

```java

Object invokeInTransaction(Method method, Object[] args) {
    Connection conn = null;
    boolean newTx = false;

    try {
        // 1. 看当前线程有没有事务
        ConnectionHolder holder = TransactionSynchronizationManager.getResource(dataSource);

        if (holder == null) {
            // 2. 没有就新开一个事务
            conn = dataSource.getConnection();
            conn.setAutoCommit(false);   // 开启事务语义
            holder = new ConnectionHolder(conn);
            TransactionSynchronizationManager.bindResource(dataSource, holder);
            newTx = true;
        } else {
            // 3. 已有事务就加入
            conn = holder.getConnection();
        }

        // 4. 执行业务方法
        Object result = method.invoke(target, args);

        // 5. 提交
        if (newTx) {
            conn.commit();
        }

        return result;
    } catch (Throwable ex) {
        // 6. 回滚
        if (newTx && conn != null) {
            conn.rollback();
        }
        throw ex;
    } finally {
        // 7. 清理
        if (newTx && conn != null) {
            try {
                conn.setAutoCommit(true); // 恢复连接池要求的默认状态
            } finally {
                TransactionSynchronizationManager.unbindResource(dataSource);
                conn.close(); // 实际通常是还回连接池。如 hikariCP 连接池
            }
        }
    }
}
```

## ResultSet 高级 API

### executeBatch()

`Statement`的 batch 本质上是把一批 SQL 一起执行
```java
con.setAutoCommit(false);
Statement stmt = con.createStatement();
stmt.addBatch("INSERT INTO COFFEES" VALUES ("japan, 49"));
stmt.addBatch("INSERT INTO COFFEES" VALUES ("america, 50"));
int[] updateCounts = stmt.executeBatch();
con.commit();
con.setAutoCommit(true);
```

`PreparedStatement`的batch，则可以拼接 insert 的多参数功能
```java
con.setAutoCommit(false);
PreparedStatement pstmt = con.prepareStatement("INSERT INTO COFFEES VALUES(?, ?))");
pstmt.setString(1, "Americano");
pstmt.setInt(2,49);
pstmt.addBatch();
pstmt.setString(1, "japan");
pstmt.setInt(2,50);
pstmt.addBatch();
int[] updateCounts = pstmt.executeBatch();
con.commit();
con.setAutoCommit(true);
```

`executeBatch()`方法的异常：
1. 中途某一条其实是`Query`（`SELECT`）
2. 中途有一条失败了

## generatedKeys —— update DML 也有 ResultSet

`insert`语句返回的结果，带上生成的主键，是一个非常常见的需求。

mybatis 帮我们封装了这个`ResultSet keys`的**获取和回填**的过程。

但我们要清楚地意识到：当我们期待**回填**时，我们虽然执行的是`executeUpdate`，但我们同时要尝试获取`update`语义下的`ResultSet`。

```java
stmt.executeUpdate(sql, Statement.RETURN_GENERATED_KEYS);
pstmt = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
// 还需要显式地取出 keys
ResultSet keys = stmt.getGeneratedKeys();
```


## MetaData —— 中间件需要格外关注的一层

- `DatabaseMetaData`：数据库系统（如 Mysql）的元数据，会决定一些**高级功能能不能用**
- `ResultSetMetaData`：ORM框架需要格外关注的，决定了**数据的列名、数据类型等**
- `ParameterMetaData`：【这个几乎不用，因为参数类型在 java 侧已经知道，不需要从服务器求证，否则会降低性能】专属于`PreparedStatement`。


### ResultSetMetaData——遍历结果集需要用的
假设你是orm框架的作者，你最重要的工作就是——把 java class 里的成员名，与数据库的列名对应起来。

鉴于 ResultSet 本身的结构，我们需要知道：列index、列名、列值类型(sqlType <=> jdbcType)

```java
ResultSetMetaData rsmd = rs.getMetaData();
int numberOfColumns = rsmd.getColumncCount();
for (int i = 1; i <= numberOfColumns; i++) {
	// 注意，列名是从 1 开始获取的。
	String columnName = rsmd.getColumnLabel(i);
	// jdbcType 是有固定 code 编码来定义的。如 int 4 -> java.sql.Types.INTEGER;
	int jdbcType = rsmd.getColumnType(i);
}
```

### DatabaseMetaData
有 150 多个属性，代表着数据库支持的各种能力。
