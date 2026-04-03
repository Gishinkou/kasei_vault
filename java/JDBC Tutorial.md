
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

