## 三件事
1. 编译器（javac）
2. 运行期类加载（ClassLoader）
3. 打包/依赖范围（Maven scope: Provided）
## java 里“出现类名”的场景

 ### 编译期：找`.class`文件

> 编译期需要考虑的问题：找不找得到具体的类定义代码。关注有没有
> 这类比到其他语言，可能是头文件签名，动态依赖的接口签名等，也可以类比到RPC的纯接口定义

### 运行期真的需要

java 运行期可以说是“懒加载”，取决于“代码路径和字节码”对这个类的**主动使用**

## Provided 的真实含义

编译期有，会在 **compile classpath** 上，可以import，可以编译通过

运行时没有，也就是声明放在那里，实现实际不存在

## java运行时，进入provided 包的入口有哪些

### 1. ClassNotFoundException：主动找类
- `Class.forName`、`loadClass`，可以简单理解为“查找运行时包文件”的主动查询
### 2. NoClassDefFoundError: 

