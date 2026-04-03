
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
#### PreparedStatement 到底持有什么

- 有`?` 占位符
- 有 `setter` 绑定参数
- **数据库可以复用执行计划**

#### 插播：数据库对一条SQL做哪些步骤
1. parseSQL: 语法层面的分析
2. optimize: SQL 优化
3. executionPlan：创建执行计划
4. return statement id：返回 `statement_id` （关键，这是后续传参数的凭据）
5. 客户端 `setInt/ setString` 等，设置参数
6. 客户端 `execute()`，将 `{参数 + statement_id}` 发出

#### 关键问题： preparedStatement，编译发生在什么位置

从上述过程可以看出，`preparedStatement`主要是通过`prepareStatement(sql)`方法，理论上会**触发一次服务器编译**，并将 `statement_id`存在内存中，作为下次访问的凭据。

但究竟是不是这样呢？让我们看一下 Mysql 文章中的 PrepareStatement 章节是怎么写的 [Mysql官方文档 15.5preparedStatements](https://dev.mysql.com/doc/refman/8.4/en/sql-prepared-statements.html)

>MySQL 8.4 provides support for server-side prepared statements. This support takes advantage of the efficient client/server binary protocol. Using prepared statements with placeholders for parameter values has the following benefits:
> - Less overhead for parsing the statement each time it is executed. Typically, database applications process large volumes of almost-identical statements, with only changes to literal or variable values in clauses such as `WHERE` for queries and deletes, `SET` for updates, and `VALUES` for inserts.
> - Protection against SQL injection attacks. The parameter values can contain unescaped SQL quote and delimiter characters.

文章中明确指出“server-side prepared statements”。这样做的好处有两点：1. 减少额外成本(overhead)，并且明确是"parsing statement"这种解析上的成本。



