
## executeUpdate 还支持DDL

`executeUpdate`不止用于增删改 DML，还用于**建表**的DDL。

## Statement 的复用

注意以下情景，`Statement stmt`被复用，需要清除可能残留的状态。
```java
stmt.executeUpdate('INSERT INTO COFFEES VALUES ('italy', 49)');
stmt.executeUpdate('INSERT INTO COFFEES VALUES ('japan', 50)');
```

