
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