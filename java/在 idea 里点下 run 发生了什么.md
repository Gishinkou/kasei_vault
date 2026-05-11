idea 里我们快速写了一个小函数脚本 `private void doSomething()`，然后写了一个 main 方法。这背后发生了什么？
```
private void doSomething() {
	int ans = 0;
	for (int i = 0; i < 10; i++) {
		ans += i;
	}
	System.out.println("0 + 1 + ... + 9 = " + ans);
}
public static void main(String[] args) {
	doSomething();
}
```

## java 的 class 与 main

每个文件（`class` 都可以有 main 吗？—— 答案是“是”


### 阶段一：编译

IDEA 会先做增量编译

```
javac -d out/production xxx/*.java
```

该阶段实际上是**对特定`.java`文件**做编译，编译的结果是`.class`文件

### 阶段二：启动 JVM

注意以下`<classpath>`展开来以后可能是classes目录/独立的jar包路径
```
java -cp <classpath> com.example.Main

java -cp /Users/you/project/target/classes:\  
/Users/you/.m2/repository/mysql/mysql-connector-j-8.0.33.jar:\  
/Users/you/.m2/repository/spring-core-5.3.30.jar \  
com.example.Main
```

#### 补充：classes 和 jar 包路径的实质
👉 jar 本质就是一个 zip 包，里面长这样：
```
mysql-connector-j-8.0.33.jar ├── com/mysql/cj/jdbc/Driver.class ├── ...
```
JVM 会：👉 “像文件系统一样”在 jar 里找 class


#### 为什么用冒号“:”——传统：路径列表分隔符

👉 在类 Unix 系统（Linux / macOS）里：

> 用 `:` 表示“路径列表分隔符”

如 `echo $PATH`，会看到
```
/usr/bin:/bin:/usr/sbin:/sbin
```

👉  在 windows 上不一样！windows 用的是分号
```
java -cp dir1;dir2;lib.jar Main
```