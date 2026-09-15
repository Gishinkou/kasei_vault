## 1. @Configuration 的作用

`@Configuration` 注解不只提示“Spring 来扫我这个类”，而是会给类内“工厂”性质的方法做CGLIB 代理，替换掉一些行为，来确保 bean 的单例性。

主要用于一个bean 方法里，注入的参数不是 `@Qualifier("masterDataSource") DataSource dataSource`，而是`this.createMasterDataSource()`这种带有`@Bean`注解的工厂方法。

如果不进行代理，则create*()方法每次会产生一个实例，会导致混乱。因此`create*()`类型的工厂构造方法会被CGLIB代理掉，确保不重复执行。

这个代理不是必要的，如果走`@Qualifier("masterDataSource") DataSource dataSource`，而不是工厂方法，就不会有重复实例化的问题。因此@Configuration 可以主动避免代理：

```
@Configuration(proxyBeanMethods = false) // 关闭 CGLIB 代理，进入“精简模式”
```

## 2. 配置扫描的控制

### 1. 配置(properties)的来源（开发者怎么写）

Spring 默认以最高优先级采纳 `application.properties` 中的配置项。
可以在任意位置（不一定在应用主类）指定扫描的 `PropertySource`，读取子配置

主配置和子配置的 level 原则：
- `application.properties`有最高优先级，**同名属性下优先取application.properties**里的
- `PropertySource=`指定的`xx.properties`，虽然同名下会被覆盖，但不同名时会和`application.properties`里的**进行拼接**，两个地方的 properties 同时取用。
- 心智模型：
	- 所有符合模式匹配的 value 项都会被采纳考量，物尽其用。
	- 在重名时优先级是父大于子，而不是子override父。

```
@Configuration

@PropertySource(value = "classpath:profile/dongdal.properties", ignoreResourceNotFound = true)

```
### 2. 配置工作的过程（spring会怎么处理）

| **特性**                     | **@ConfigurationProperties (按前缀装配)**                         | **@Value (逐个注入)**                             |
| -------------------------- | ------------------------------------------------------------ | --------------------------------------------- |
| **设计理念**                   | **面向对象**，强类型，适合批量、复杂的结构化配置。                                  | **面向属性**，适合零散的、单一的配置值提取。                      |
| **颗粒度**                    | **类级别** (绑定一个前缀下的所有属性)。                                      | **字段/参数级别** (每次只能指明一个 key)。                   |
| **松散绑定 (Relaxed Binding)** | **支持**。配置写 `max-connections`，Java 里写 `maxConnections`，能自动匹配。 | **不支持**。必须严格写 `@Value("${max-connections}")`。 |
| **SpEL (Spring 表达式)**      | **不支持**。纯粹的属性名映射。                                            | **支持**。比如 `@Value("#{11 * 2}")` 或动态运算。        |
| **复杂类型 (List, Map, 嵌套对象)** | **完美支持**。配置里写数组/字典，能直接转成 Java 的 List/Map。                    | **非常麻烦**。通常需要自己用分隔符切分字符串。                     |
| **JSR-303 数据校验**           | **支持**。可以在字段上加 `@NotNull`, `@Min` 等，启动时校验配置。                 | **不支持**。                                      |

配置扫描主要有`@ConfigurationProperties`和`@Value`两种方式。前者根据固定前缀对象化，后者是精确匹配。前者会有配置风格的模糊化处理，后者不会。