以下是 `BasicDataSource` 全部可配置项清单，来源于 `BasicDataSourceFactory.java` 和 `configuration.xml`： [1](#0-0) [2](#0-1) 

---

## 一、JDBC 连接基础

| 参数                           | 默认值 | 选择   | 说明                                                         |                     |
| ---------------------------- | --- | ---- | ---------------------------------------------------------- | ------------------- |
| `username`                   | —   |      | 连接数据库的用户名                                                  |                     |
| `password`                   | —   |      | 连接数据库的密码                                                   |                     |
| `url`                        | —   |      | JDBC 连接 URL                                                |                     |
| `driverClassName`            | —   | 🔒默认 | JDBC 驱动的完整类名                                               |                     |
| `connectionFactoryClassName` | —   | 🔒默认 | 自定义 `ConnectionFactory` 实现类名                               |                     |
| `connectionProperties`       | —   |      | 传给驱动的额外连接属性，格式：`key=value;key2=value2`（user/password 无需包含） | [3](#0-2) [4](#0-3) |

---

## 二、连接默认行为

| 参数                            | 默认值          | 选择   | 说明                                                                                           |                     |
| ----------------------------- | ------------ | ---- | -------------------------------------------------------------------------------------------- | ------------------- |
| `defaultAutoCommit`           | 驱动默认         | 🔒默认 | 连接的默认 auto-commit 状态，未设置则不调用 `setAutoCommit`                                                 |                     |
| `defaultReadOnly`             | 驱动默认         | 🔒默认 | 连接的默认只读状态，未设置则不调用 `setReadOnly`                                                              |                     |
| `defaultTransactionIsolation` | 驱动默认         | 🔒默认 | 默认事务隔离级别：`NONE` / `READ_COMMITTED` / `READ_UNCOMMITTED` / `REPEATABLE_READ` / `SERIALIZABLE` |                     |
| `defaultCatalog`              | —            | 🔒默认 | 连接的默认 catalog                                                                                |                     |
| `defaultSchema`               | —            | 🔒默认 | 连接的默认 schema                                                                                 |                     |
| `defaultQueryTimeout`         | `null`（驱动默认） | 🔒默认 | Statement 的默认查询超时（秒），null 表示使用驱动默认                                                           |                     |
| `cacheState`                  | `true`       | 🔒默认 | 是否缓存 readOnly/autoCommit 状态以减少数据库查询；若直接操作底层连接修改了这些状态，应设为 false                               |                     |
| `enableAutoCommitOnReturn`    | `true`       | 🔒默认 | 连接归还时若 autoCommit=false，是否自动重置为 true                                                         |                     |
| `rollbackOnReturn`            | `true`       | 🔒默认 | 连接归还时若 autoCommit=false 且非只读，是否自动 rollback                                                   | [5](#0-4) [6](#0-5) |
以下只发生在 connection 第一次创建完成时：

| 参数                   | 默认值    | 选择   | 说明                              |                         |
| -------------------- | ------ | ---- | ------------------------------- | ----------------------- |
| `connectionInitSqls` | `null` | 🔒默认 | 物理连接首次创建时执行的 SQL 列表（分号分隔），仅执行一次 | [17](#0-16) [18](#0-17) |
- 注意`connectionInitSqls`不是说开始执行`SELECT 1`，应用场景更多是初始化连接状态
	- 设置自动提交：`SET autocommit=1`
	- 设置时区：`SET time_zone= '+08:00'`

---

## 三、连接池大小控制

| 参数              | 默认值        | 选择      | 说明                                |                     |
| --------------- | ---------- | ------- | --------------------------------- | ------------------- |
| `initialSize`   | `0`        | 🔄待定    | 池启动时预创建的连接数                       |                     |
| `maxTotal`      | `8`        | 🔄待定    | 池中最大活跃连接数，负数表示无限制                 |                     |
| `maxIdle`       | `8`        | 🔄待定    | 池中最大空闲连接数，负数表示无限制                 |                     |
| `minIdle`       | `0`        | 🔄待定    | 池中最小空闲连接数，0 表示不保留                 |                     |
| `maxWaitMillis` | `-1`（无限等待） | ✅保持2000 | 无可用连接时最长等待毫秒数，-1 表示无限等待，超时抛异常     |                     |
| `lifo`          | `true`     | 🔒默认    | true=LIFO（最近使用优先），false=FIFO 队列顺序 | [7](#0-6) [8](#0-7) |
- **初始化过程**：
	- 懒加载：`BasicDataSource.getConnection()`懒初始化进入 createDataSource()
	- 连接池初始构建：工厂先设置`poolPreparedStatements`和`maxOpenPreparedStatement`这两个参数，然后调用`createPoolableConnecitonFactory`，把其他参数一并set入。
		- 注意其中一个参数影响工厂调用：`registerConnectionMBean`，指MBean监控关键类的注入，不开启则注入null，跳过该逻辑。
	- 预建连接：`initialSize`一次生效（`connectionPool.addObjects(initialSize)`，调用的是底层的通用对象池里的add方法，也就是add指定数量通用对象的方法
	- 开启池维护（保活逻辑块）：用来启动池子维护功能，但里面只设置了`setDurationBetweenEvictionRuns`和第五章空闲连接驱逐里的变量产生了关联。
- 借连接【借用时做很多事，热路径比较重，行为比较显式】：
	- `maxTotal`，`maxWaitMillis`在最大数量和最大耗时上控制获取连接是否失败。超容量则进入阻塞等待，等待时间达到上限就放弃。
	- 发生借用校验`testOnBorrow`，接下来会尝试执行`validationQuery`（默认null）和`validationQueryTimeout`（默认无超时）。
		- 泄露回收`removeAbandonedOnBorrow`默认是false，`removeAbandonedTimeout`是默认是300秒。关于泄露回收，还有两个日志、追踪选项`logAbandoned`和`abandonedUsageTracking`。[TODO: 说到底，泄露回收(以abandon作为关键词)]到底做什么。`removeAbandonedOnBorrow=true` 不是无条件回收，它还依赖 `getNumActive() > getMaxTotal()-3` 且 `getNumIdle() < 2` 这两个条件。对中间件而言，DBCP 的 borrow wait 与 abandoned reclaim 其实是两套背压机制，不能同时激进打开
		- [TODO: fastFailValidation, disconnectionSqlCodes, `disconnectionIgnoreSqlCodes`]`fastFailValidation=true` 只有与 SQLState 分类配置联动时，才会把“已判定断连”的连接在后续验证时直接 fail fast。
- 归还连接时的事务状态残留问题
	- `rollbackOnReturn` 默认 true、`autoCommitOnReturn` 默认 true、`cacheState` 默认 true
		- `autoCommitOnReturn`不是配置而是一个状态记录。
		- `rollbackOnReturn`为true时，会回滚未提交事务。因为此时理论上，上层业务调用已经调了close，丢失了对这个连接的引用。这个连接务必要回收掉。
		- `cacheState`的作用是把`autoCommit/readOnly`的状态记录在本地，而不用和数据库进行网络IO。
	- 【一个待验证的观点】：即使不开启归还时忘记提交的事务的rollback，也可能在连接下次`setAutoCommit`时，触发隐式的事务提交（MySQL是这样的）
- 归还连接时的空闲治理问题。
	- 归还时首先做`testOnReturn`检验，检验失败后会触发`ensureIdle(1,false)`来对最小空闲连接数进行确保。
		- 注意这里有一个`maxIdle`的概念，如果归还的连接数超过了`maxIdle`，会触发销毁而不是回到idle deque。
		- 注意这里的`ensureIdle`的第一个参数是最小连接数预期，也就是说，`testOnReturn`只确保至少一个空闲连接存在。 
	- 归还时的连接存活时间检验机制：
		- 有两个配置：（软规则）`softMinEvictableIdleTimeMillis`和 （硬规则）`minEvictableIdleTimeMillis`
			- 硬限制可能导致连接被清除到`minIdle`以下，而软限制只在连接数超越`minIdle`时可以生效。**软限制的语义是允许提前清理**
			- **软限制**的时间**短**于**硬限制**
			- 多余连接提早被清除，而最小连接数保活30分钟。
- LIFO：先来后出这样一个限制实际实现了冷热分层。
	- 新连接被频繁复用，老连接则一直闲置
	- 定期的 驱逐会发生在老连接上。
---

## 四、连接验证

| 参数                       | 默认值     | 说明                                                           |                      |
| ------------------------ | ------- | ------------------------------------------------------------ | -------------------- |
| `validationQuery`        | —       | 验证连接有效性的 SQL（必须是返回至少一行的 SELECT），未设置则用 `Connection.isValid()` |                      |
| `validationQueryTimeout` | 无超时     | 验证查询的超时秒数，正值才生效                                              |                      |
| `testOnCreate`           | `false` | 连接创建后是否立即验证，验证失败则借用操作失败                                      |                      |
| `testOnBorrow`           | `true`  | 从池中借用连接前是否验证，验证失败则丢弃并重试                                      |                      |
| `testOnReturn`           | `false` | 连接归还到池时是否验证                                                  |                      |
| `testWhileIdle`          | `false` | 空闲驱逐线程运行时是否验证空闲连接，验证失败则丢弃                                    | [9](#0-8) [10](#0-9) |


---

## 五、空闲连接驱逐（Eviction）

| 参数                               | 默认值             | 说明                                                                   |                         |
| -------------------------------- | --------------- | -------------------------------------------------------------------- | ----------------------- |
| `timeBetweenEvictionRunsMillis`  | `-1`（不运行）       | 空闲驱逐线程运行间隔毫秒数，非正值则不启动驱逐线程                                            |                         |
| `numTestsPerEvictionRun`         | `3`             | 每次驱逐线程运行时检查的连接数                                                      |                         |
| `minEvictableIdleTimeMillis`     | `1800000`（30分钟） | 连接在池中空闲超过此时长（毫秒）才有资格被驱逐                                              |                         |
| `softMinEvictableIdleTimeMillis` | `-1`            | 类似上项，但额外要求池中空闲连接数超过 `minIdle` 才驱逐；`minEvictableIdleTimeMillis` 优先级更高 |                         |
| `evictionPolicyClassName`        | 默认策略            | 自定义驱逐策略的完整类名，需实现 `EvictionPolicy` 接口                                 |                         |
| `maxConnLifetimeMillis`          | `-1`（无限）        | 连接最大存活时长（毫秒），超过后在下次激活/钝化/验证时关闭，≤0 表示无限                               |                         |
| `logExpiredConnections`          | `true`          | 是否记录因超过 `maxConnLifetimeMillis` 而被关闭的连接日志                            | [11](#0-10) [12](#0-11) |
|                                  |                 |                                                                      |                         |
- Eviction驱逐机制（注意只驱逐idle连接）：
	- `timeBetweenEvictionRunsMillis`这个是核心开关，需要大于0，才启动，否则无任何行为。
	- 会启动一个`后台线程（Evictor）`，周期性地扫描`idle`连接。（注意只驱逐idle连接）。
	- 测试参数为`testWhileIdle`
	- 关键的**批量参数**，是一个`numTestsPerEvictionRun`，这是一种**渐进式扫描**，而不是全量的。
	- 【关键】连接最大存活时间`maxConnLifetimeMillis`，默认是无限，不适合直接使用。
---

## 六、废弃连接处理（Abandoned Connection）

| 参数                             | 默认值      | 说明                                                     |                         |
| ------------------------------ | -------- | ------------------------------------------------------ | ----------------------- |
| `removeAbandonedOnBorrow`      | `false`  | 借用连接时若满足条件（活跃数 > maxTotal-3 且空闲数 < 2）则清理废弃连接           |                         |
| `removeAbandonedOnMaintenance` | `false`  | 驱逐线程运行结束后清理废弃连接（需 `timeBetweenEvictionRunsMillis` > 0） |                         |
| `removeAbandonedTimeout`       | `300`（秒） | 连接超过此秒数未使用则视为废弃（执行 Statement 会重置计时）                    |                         |
| `logAbandoned`                 | `false`  | 是否记录废弃连接/Statement 的堆栈信息（有性能开销）                        |                         |
| `abandonedUsageTracking`       | `false`  | 是否记录每次方法调用的堆栈以辅助调试废弃连接（开销显著）                           | [13](#0-12) [14](#0-13) |

- 如何定义废弃连接，废弃连接有什么问题
	- 废弃连接是**连接已经借出**，但**长时间没有归还**。这主要有连接泄露的风险。
		- 但听说有些业务会有**超过两个小时**的超长事务，直觉上会被这个东西判定成废弃连接，导致失败？
		- 事实上：判定废弃连接主要依据**lastUsed**到当前时间的差值，是否大于`removeAbandonedTimeout`。而根据文档：DBCP更新 `lastUsed`的主要依据是：
			- 创建 Statement
			- 创建 PreparedStatement
			- 创建 CallableStatement
			- 使用这些 Statement 执行 query/update，也就是 execute 系列方法
		- 可能会被误判的场景：
			- 一个**超长事务同时**涉及Mysql和其他类型的数据存储、消息中间件、文件系统等，**时间花在了其他IO或计算任务**上。数据库statement本身可能不再继续活跃了，可能在等待任务结束，或等待汇总完结果落库。这种情况就可能被**误判为废弃连接**
---

## 七、PreparedStatement 池化

| 参数                           | 默认值     | 说明                                                |                         |
| ---------------------------- | ------- | ------------------------------------------------- | ----------------------- |
| `poolPreparedStatements`     | `false` | 是否启用 PreparedStatement 池化（同时包含 CallableStatement） |                         |
| `maxOpenPreparedStatements`  | 无限制     | Statement 池中最大同时开放的 Statement 数，负数表示无限制           |                         |
| `clearStatementPoolOnReturn` | `false` | 连接归还时是否清空其 Statement 池                            | [15](#0-14) [16](#0-15) |
|                              |         |                                                   |                         |
- PreparedStatement池化的作用范围
	- 这是一个`connection`层级的缓存池，而不是应用全局的。
	- 也就是每个连接都会有一个自己的缓存池。连接数为100就是100倍缓存池。
- PreparedStatement池化的内存占用
	- 以20个连接，100个连接池规模去估计，就是2000个PS缓存池，假如缓存100个preparedStatement
		- 以一个preparedStatement 1KB-5KB来计算，大约占用`200MB`到`1GB`
		- 每连接建议 20~50个 PS缓存数量
- 这里对`PreparedStatement`做的**池化**到底解决什么问题？
	- `PreparedStatement`本身就有缓存的设计意图，一个statement预编译后只需替换参数，少走很多流程
	- 但其问题在于，它不能**跨调用复用**，通常只是一个业务方法里的多个参数之间生效。
	- 将其池化，可以在多次调用之间复用，减少编译成本。
	- 需要区分：`preparedStatement`的缓存是**发生在client侧**还是**server侧**。
		- `JDBC connector`实现中，默认是关闭服务侧缓存的（`useServerPrepStmts`=false)
		- 也就是说，不考虑池化时，preparedStatement 本身的作用，主要是JVM逻辑成本，这包括拼SQL，替换参数，设置执行前的一些上下文信息等。
		- 池化后则是进一步跨调用优化这层成本。
---


---

## 八、快速失败验证（Fast Fail Validation）

| 参数                            | 默认值     | 说明                                                                        |                         |
| ----------------------------- | ------- | ------------------------------------------------------------------------- | ----------------------- |
| `fastFailValidation`          | `false` | 对已抛出"致命" SQLException 的连接，验证立即失败，不再调用 `isValid` 或执行验证 SQL                 |                         |
| `disconnectionSqlCodes`       | `null`  | 逗号分隔的 SQL State 码列表，视为致命断连错误（需 `fastFailValidation=true`）                 |                         |
| `disconnectionIgnoreSqlCodes` | `null`  | 逗号分隔的 SQL State 码列表，即使匹配致命条件也忽略（需 `fastFailValidation=true`，since 2.13.0） | [19](#0-18) [20](#0-19) |
- `fastfail`机制
	- **如何在“连接已经坏掉”的情况下，避免再做一次无意义的验证**
	- `disconnectionSqlCodes`是一些预定义的SQL states码列表，如
		- disconnectionSqlCodes = "08S01,08003,08006,..."
		- 08S01 -> communication link failure  
		- 08003 -> connection does not exist  
		- 08006 -> connection failure
	- 出现这种指向连接不可用的SQLException，则直接标记链接损坏
		- 对于已经表现出损坏特征的连接：避免了验证代价

---

## 九、JMX 监控

| 参数                        | 默认值    | 说明                                                   |                         |
| ------------------------- | ------ | ---------------------------------------------------- | ----------------------- |
| `jmxName`                 | —      | 将 DataSource 注册为 JMX MBean 的名称，需符合 JMX ObjectName 语法 |                         |
| `registerConnectionMBean` | `true` | 是否为每个连接注册 JMX MBean                                  | [21](#0-20) [22](#0-21) |

---

## 十、其他

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `accessToUnderlyingConnectionAllowed` | `false` | 是否允许通过 `DelegatingConnection.getInnermostDelegate()` 访问底层原始连接（有风险，谨慎使用） | [23](#0-22) [24](#0-23) 

---

> **注意**：DBCP 1.x 中的 `maxActive`、`removeAbandoned`、`maxWait` 在 DBCP 2.x 中已废弃，分别由 `maxTotal`、`removeAbandonedOnBorrow`/`removeAbandonedOnMaintenance`、`maxWaitMillis` 替代。 [25](#0-24)

### Citations

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSourceFactory.java (L88-95)
```java
    private static final String PROP_PASSWORD = Constants.KEY_PASSWORD;
    private static final String PROP_URL = "url";
    private static final String PROP_USER_NAME = "username";
    private static final String PROP_VALIDATION_QUERY = "validationQuery";
    private static final String PROP_VALIDATION_QUERY_TIMEOUT = "validationQueryTimeout";
    private static final String PROP_JMX_NAME = "jmxName";
    private static final String PROP_REGISTER_CONNECTION_MBEAN = "registerConnectionMBean";
    private static final String PROP_CONNECTION_FACTORY_CLASS_NAME = "connectionFactoryClassName";
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSourceFactory.java (L101-106)
```java
    private static final String PROP_ACCESS_TO_UNDERLYING_CONNECTION_ALLOWED = "accessToUnderlyingConnectionAllowed";
    private static final String PROP_REMOVE_ABANDONED_ON_BORROW = "removeAbandonedOnBorrow";
    private static final String PROP_REMOVE_ABANDONED_ON_MAINTENANCE = "removeAbandonedOnMaintenance";
    private static final String PROP_REMOVE_ABANDONED_TIMEOUT = "removeAbandonedTimeout";
    private static final String PROP_LOG_ABANDONED = "logAbandoned";
    private static final String PROP_ABANDONED_USAGE_TRACKING = "abandonedUsageTracking";
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSourceFactory.java (L116-132)
```java
    private static final String PROP_FAST_FAIL_VALIDATION = "fastFailValidation";

    /**
     * Value string must be of the form [STATE_CODE,]*
     */
    private static final String PROP_DISCONNECTION_SQL_CODES = "disconnectionSqlCodes";

    /**
     * Property key for specifying the SQL State codes that should be ignored during disconnection checks.
     * <p>
     * The value for this property must be a comma-separated string of SQL State codes, where each code represents
     * a state that will be excluded from being treated as a fatal disconnection. The expected format is a series
     * of SQL State codes separated by commas, with no spaces between them (e.g., "08003,08004").
     * </p>
     * @since 2.13.0
     */
    private static final String PROP_DISCONNECTION_IGNORE_SQL_CODES = "disconnectionIgnoreSqlCodes";
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSourceFactory.java (L138-183)
```java
    private static final String NUPROP_MAX_ACTIVE = "maxActive";
    private static final String NUPROP_REMOVE_ABANDONED = "removeAbandoned";
    private static final String NUPROP_MAXWAIT = "maxWait";

    /*
     * Block with properties expected in a DataSource This props will not be listed as ignored - we know that they may
     * appear in Resource, and not listing them as ignored.
     */
    private static final String SILENT_PROP_FACTORY = "factory";
    private static final String SILENT_PROP_SCOPE = "scope";
    private static final String SILENT_PROP_SINGLETON = "singleton";
    private static final String SILENT_PROP_AUTH = "auth";

    private static final List<String> ALL_PROPERTY_NAMES = Arrays.asList(PROP_DEFAULT_AUTO_COMMIT, PROP_DEFAULT_READ_ONLY,
            PROP_DEFAULT_TRANSACTION_ISOLATION, PROP_DEFAULT_CATALOG, PROP_DEFAULT_SCHEMA, PROP_CACHE_STATE,
            PROP_DRIVER_CLASS_NAME, PROP_LIFO, PROP_MAX_TOTAL, PROP_MAX_IDLE, PROP_MIN_IDLE, PROP_INITIAL_SIZE,
            PROP_MAX_WAIT_MILLIS, PROP_TEST_ON_CREATE, PROP_TEST_ON_BORROW, PROP_TEST_ON_RETURN,
            PROP_TIME_BETWEEN_EVICTION_RUNS_MILLIS, PROP_NUM_TESTS_PER_EVICTION_RUN, PROP_MIN_EVICTABLE_IDLE_TIME_MILLIS,
            PROP_SOFT_MIN_EVICTABLE_IDLE_TIME_MILLIS, PROP_EVICTION_POLICY_CLASS_NAME, PROP_TEST_WHILE_IDLE, PROP_PASSWORD,
            PROP_URL, PROP_USER_NAME, PROP_VALIDATION_QUERY, PROP_VALIDATION_QUERY_TIMEOUT, PROP_CONNECTION_INIT_SQLS,
            PROP_ACCESS_TO_UNDERLYING_CONNECTION_ALLOWED, PROP_REMOVE_ABANDONED_ON_BORROW, PROP_REMOVE_ABANDONED_ON_MAINTENANCE,
            PROP_REMOVE_ABANDONED_TIMEOUT, PROP_LOG_ABANDONED, PROP_ABANDONED_USAGE_TRACKING, PROP_POOL_PREPARED_STATEMENTS,
            PROP_CLEAR_STATEMENT_POOL_ON_RETURN,
            PROP_MAX_OPEN_PREPARED_STATEMENTS, PROP_CONNECTION_PROPERTIES, PROP_MAX_CONN_LIFETIME_MILLIS,
            PROP_LOG_EXPIRED_CONNECTIONS, PROP_ROLLBACK_ON_RETURN, PROP_ENABLE_AUTO_COMMIT_ON_RETURN,
            PROP_DEFAULT_QUERY_TIMEOUT, PROP_FAST_FAIL_VALIDATION, PROP_DISCONNECTION_SQL_CODES, PROP_DISCONNECTION_IGNORE_SQL_CODES,
            PROP_JMX_NAME, PROP_REGISTER_CONNECTION_MBEAN, PROP_CONNECTION_FACTORY_CLASS_NAME);

    /**
     * Obsolete properties from DBCP 1.x. with warning strings suggesting new properties. LinkedHashMap will guarantee
     * that properties will be listed to output in order of insertion into map.
     */
    private static final Map<String, String> NUPROP_WARNTEXT = new LinkedHashMap<>();

    static {
        NUPROP_WARNTEXT.put(NUPROP_MAX_ACTIVE,
                "Property " + NUPROP_MAX_ACTIVE + " is not used in DBCP2, use " + PROP_MAX_TOTAL + " instead. "
                        + PROP_MAX_TOTAL + " default value is " + GenericObjectPoolConfig.DEFAULT_MAX_TOTAL + ".");
        NUPROP_WARNTEXT.put(NUPROP_REMOVE_ABANDONED,
                "Property " + NUPROP_REMOVE_ABANDONED + " is not used in DBCP2," + " use one or both of "
                        + PROP_REMOVE_ABANDONED_ON_BORROW + " or " + PROP_REMOVE_ABANDONED_ON_MAINTENANCE + " instead. "
                        + "Both have default value set to false.");
        NUPROP_WARNTEXT.put(NUPROP_MAXWAIT,
                "Property " + NUPROP_MAXWAIT + " is not used in DBCP2" + " , use " + PROP_MAX_WAIT_MILLIS + " instead. "
                        + PROP_MAX_WAIT_MILLIS + " default value is " + BaseObjectPoolConfig.DEFAULT_MAX_WAIT
                        + ".");
```

**File:** src/site/xdoc/configuration.xml (L50-527)
```text
<section name="BasicDataSource Configuration Parameters">

<table>
<tr><th>Parameter</th><th>Description</th></tr>
<tr>
   <td>username</td>
   <td>The connection user name to be passed to our JDBC driver to establish a connection.</td>
</tr>
<tr>
   <td>password</td>
   <td>The connection password to be passed to our JDBC driver to establish a connection.</td>
</tr>
<tr>
   <td>url</td>
   <td>The connection URL to be passed to our JDBC driver to establish a connection.</td>
</tr>
<tr>
   <td>driverClassName</td>
   <td>The fully qualified Java class name of the JDBC driver to be used.</td>
</tr>
<tr>
   <td>connectionProperties</td>
   <td>The connection properties that will be sent to our JDBC driver when establishing new connections.
       <br/>Format of the string must be [propertyName=property;]*
       <br/><strong>NOTE</strong> - The "user" and "password" properties will be passed explicitly, 
       so they do not need to be included here.
   </td>
</tr>
</table>


<table>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr>
   <td>defaultAutoCommit</td>
   <td>driver default</td>
   <td>The default auto-commit state of connections created by this pool.
       If not set then the setAutoCommit method will not be called.
   </td>
</tr>
<tr>
   <td>defaultReadOnly</td>
   <td>driver default</td>
   <td>The default read-only state of connections created by this pool.
       If not set then the setReadOnly method will not be called.
       (Some drivers don't support read only mode, ex: Informix)
   </td>
</tr>
<tr>
   <td>defaultTransactionIsolation</td>
   <td>driver default</td>
   <td>The default TransactionIsolation state of connections created by this pool.
       One of the following: (see 
       <a href="http://java.sun.com/j2se/1.4.2/docs/api/java/sql/Connection.html#field_summary">javadoc</a>)
       <ul>
          <li>NONE</li>
          <li>READ_COMMITTED</li>
          <li>READ_UNCOMMITTED</li>
          <li>REPEATABLE_READ</li>
          <li>SERIALIZABLE</li>
       </ul>
   </td>
</tr>
<tr>
   <td>defaultCatalog</td>
   <td></td>
   <td>The default catalog of connections created by this pool.</td>
</tr>
<tr>
  <td>cacheState</td>
  <td>true</td>
  <td>If true, the pooled connection will cache the current readOnly and
      autoCommit settings when first read or written and on all subsequent
      writes. This removes the need for additional database queries for any
      further calls to the getter. If the underlying connection is accessed
      directly and the readOnly and/or autoCommit settings changed the cached
      values will not reflect the current state. In this case, caching should be
      disabled by setting this attribute to false.</td>
</tr>
<tr>
  <td>defaultQueryTimeout</td>
  <td>null</td>
  <td>If non-null, the value of this <code>Integer</code> property determines
      the query timeout that will be used for Statements created from
      connections managed by the pool. <code>null</code> means that the driver
      default will be used.</td>
</tr>
<tr>
  <td>enableAutoCommitOnReturn</td>
  <td>true</td>
  <td>If true, connections being returned to the pool will be checked and configured with
      <code>Connection.setAutoCommit(true)</code> if the auto commit setting is
      <code>false</code> when the connection is returned.</td>
</tr>
<tr>
  <td>rollbackOnReturn</td>
  <td>true</td>
  <td>True means a connection will be rolled back when returned to the pool if
      auto commit is not enabled and the connection is not read-only.</td>
</tr>
</table>


<table>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr>
   <td>initialSize</td>
   <td>0</td>
   <td>
      The initial number of connections that are created when the pool
      is started.
      <br/>Since: 1.2
   </td>
</tr>
<tr>
   <td>maxTotal</td>
   <td>8</td>
   <td>
      The maximum number of active connections that can be allocated from
      this pool at the same time, or negative for no limit.
   </td>
</tr>
<tr>
   <td>maxIdle</td>
   <td>8</td>
   <td>
      The maximum number of connections that can remain idle in the
      pool, without extra ones being released, or negative for no limit.
   </td>
</tr>
<tr>
   <td>minIdle</td>
   <td>0</td>
   <td>
      The minimum number of connections that can remain idle in the
      pool, without extra ones being created, or zero to create none.
   </td>
</tr>
<tr>
   <td>maxWaitMillis</td>
   <td>indefinitely</td>
   <td>
      The maximum number of milliseconds that the pool will wait (when there
      are no available connections) for a connection to be returned before
      throwing an exception, or -1 to wait indefinitely.
   </td>
</tr>
</table>
<p>
<img src="images/icon_warning_sml.gif" alt="Warning"/>
<strong>NOTE</strong>: If maxIdle is set too low on heavily loaded systems it is
possible you will see connections being closed and almost immediately new
connections being opened. This is a result of the active threads momentarily
closing connections faster than they are opening them, causing the number of
idle connections to rise above maxIdle. The best value for maxIdle for heavily
loaded system will vary but the default is a good starting point.
</p>


<table>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr>
   <td>validationQuery</td>
   <td></td>
   <td>
The SQL query that will be used to validate connections from this pool
before returning them to the caller.  If specified, this query
<strong>MUST</strong> be an SQL SELECT statement that returns at least
one row. If not specified, connections will be validation by calling the
isValid() method.
   </td>
</tr>
<tr>
  <td>validationQueryTimeout</td>
  <td>no timeout</td>
  <td>The timeout in seconds before connection validation queries fail. If set
      to a positive value, this value is passed to the driver via the
      <code>setQueryTimeout</code> method of the <code>Statement</code>
      used to execute the validation query.</td>
</tr>
<tr>
   <td>testOnCreate</td>
   <td>false</td>
   <td>
      The indication of whether objects will be validated after creation. If the
      object fails to validate, the borrow attempt that triggered the object
      creation will fail.
   </td>
</tr>
<tr>
   <td>testOnBorrow</td>
   <td>true</td>
   <td>
      The indication of whether objects will be validated before being
      borrowed from the pool.  If the object fails to validate, it will be
      dropped from the pool, and we will attempt to borrow another.
   </td>
</tr>
<tr>
   <td>testOnReturn</td>
   <td>false</td>
   <td>
      The indication of whether objects will be validated before being
      returned to the pool.
   </td>
</tr>
<tr>
   <td>testWhileIdle</td>
   <td>false</td>
   <td>
      The indication of whether objects will be validated by the idle object
      evictor (if any).  If an object fails to validate, it will be dropped
      from the pool.
   </td>
</tr>
<tr>
   <td>timeBetweenEvictionRunsMillis</td>
   <td>-1</td>
   <td>
      The number of milliseconds to sleep between runs of the idle object
      evictor thread.  When non-positive, no idle object evictor thread will
      be run.
   </td>
</tr>
<tr>
   <td>numTestsPerEvictionRun</td>
   <td>3</td>
   <td>
      The number of objects to examine during each run of the idle object
      evictor thread (if any).
   </td>
</tr>
<tr>
   <td>minEvictableIdleTimeMillis</td>
   <td>1000 * 60 * 30</td>
   <td>
      The minimum amount of time an object may sit idle in the pool before it
      is eligible for eviction by the idle object evictor (if any).
   </td>
</tr>
<tr>
   <td>softMinEvictableIdleTimeMillis</td>
   <td>-1</td>
   <td>
      The minimum amount of time a connection may sit idle in the pool before
      it is eligible for eviction by the idle connection evictor, with
      the extra condition that at least "minIdle" connections remain in the
      pool. When minEvictableIdleTimeMillis is set to a positive value,
      minEvictableIdleTimeMillis is examined first by the idle 
      connection evictor - i.e. when idle connections are visited by the
      evictor, idle time is first compared against minEvictableIdleTimeMillis
      (without considering the number of idle connections in the pool) and then
      against softMinEvictableIdleTimeMillis, including the minIdle constraint.
   </td>
</tr>
<tr>
   <td>maxConnLifetimeMillis</td>
   <td>-1</td>
   <td>
      The maximum lifetime in milliseconds of a connection. After this time is
      exceeded the connection will fail the next activation, passivation or
      validation test. A value of zero or less means the connection has an
      infinite lifetime.
   </td>
</tr>
<tr>
   <td>logExpiredConnections</td>
   <td>true</td>
   <td>
      Flag to log a message indicating that a connection is being closed by the
      pool due to maxConnLifetimeMillis exceeded. Set this property to false
      to suppress expired connection logging that is turned on by default.
   </td>
</tr>
<tr>
   <td>connectionInitSqls</td>
   <td>null</td>
   <td>
      A Collection of SQL statements that will be used to initialize physical 
      connections when they are first created.  These statements are executed
      only once - when the configured connection factory creates the connection.
   </td>
</tr>
<tr>
   <td>lifo</td>
   <td>true</td>
   <td>
      True means that borrowObject returns the most recently used ("last in")
      connection in the pool (if there are idle connections available).  False
      means that the pool behaves as a FIFO queue - connections are taken from
      the idle instance pool in the order that they are returned to the pool.
   </td>
</tr>
</table>

<table>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr><tr>
   <td>poolPreparedStatements</td>
   <td>false</td>
   <td>Enable prepared statement pooling for this pool.</td>
</tr>
<tr>
   <td>maxOpenPreparedStatements</td>
   <td>unlimited</td>
   <td>
      The maximum number of open statements that can be allocated from
      the statement pool at the same time, or negative for no limit.
   </td>
</tr>
</table>
<p>
<img src="images/icon_info_sml.gif" alt="Info"/>
This component has also the ability to pool PreparedStatements.
When enabled a statement pool will be created for each Connection
and PreparedStatements created by one of the following methods will be pooled:
</p>
<ul>
   <li>public PreparedStatement prepareStatement(String sql)</li>
   <li>public PreparedStatement prepareStatement(String sql, int resultSetType, int resultSetConcurrency)</li>
</ul>
<p>
<img src="images/icon_warning_sml.gif" alt="Warning"/>
<strong>NOTE</strong> - Make sure your connection has some resources left for the other statements.
Pooling PreparedStatements may keep their cursors open in the database, causing a connection to run out of cursors,
especially if maxOpenPreparedStatements is left at the default (unlimited) and an application opens a large number
of different PreparedStatements per connection. To avoid this problem, maxOpenPreparedStatements should be set to a
value less than the maximum number of cursors that can be open on a Connection.
</p>

<table>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr><tr>
   <td>accessToUnderlyingConnectionAllowed</td>
   <td>false</td>
   <td>Controls if the PoolGuard allows access to the underlying connection.</td>
</tr>
</table>
<p>When allowed you can access the underlying connection using the following construct:</p>
<source>
    Connection conn = ds.getConnection();
    Connection dconn = ((DelegatingConnection) conn).getInnermostDelegate();
    ...
    conn.close()
</source>
<p>
<img src="images/icon_info_sml.gif" alt="Info"/>
Default is false, it is a potential dangerous operation and misbehaving programs can do harmful things. (closing the underlying or continue using it when the guarded connection is already closed)
Be careful and only use when you need direct access to driver specific extensions.
</p>
<p>
<img src="images/icon_warning_sml.gif" alt="Warning"/>
<b>NOTE:</b> Do not close the underlying connection, only the original one.
</p>

<table>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr>
   <td>removeAbandonedOnMaintenance <br/>
       removeAbandonedOnBorrow
   </td>
   <td>false</td>
   <td>
      Flags to remove abandoned connections if they exceed the
      removeAbandonedTimout.<br/>
      A connection is considered abandoned and eligible
      for removal if it has not been used for longer than removeAbandonedTimeout.<br/>
      Creating a Statement, PreparedStatement or CallableStatement or using
      one of these to execute a query (using one of the execute methods)
      resets the lastUsed property of the parent connection.<br/>
      Setting one or both of these to true can recover db connections from poorly written
      applications which fail to close connections.<br/>
      Setting removeAbandonedOnMaintenance to true removes abandoned connections on the
      maintenance cycle (when eviction ends). This property has no effect unless maintenance
      is enabled by setting timeBetweenEvictionRunsMillis to a positive value. <br/>
      If removeAbandonedOnBorrow is true, abandoned connections are removed each time
      a connection is borrowed from the pool, with the additional requirements that
      <ul><li>getNumActive() &gt; getMaxTotal() - 3; and</li>
          <li>getNumIdle() &lt; 2 </li></ul>
   </td>
</tr>
<tr>
   <td>removeAbandonedTimeout</td>
   <td>300</td>
   <td>Timeout in <b>seconds</b> before an abandoned connection can be removed.</td>
</tr>
<tr>
   <td>logAbandoned</td>
   <td>false</td>
   <td>
      Flag to log stack traces for application code which abandoned
      a Statement or Connection.<br/>
      Logging of abandoned Statements and Connections adds overhead
      for every Connection open or new Statement because a stack   
      trace has to be generated.  
   </td>
</tr>
<tr>
   <td>abandonedUsageTracking</td>
   <td>false</td>
   <td>
      If true, the connection pool records a stack trace every time a method is called on a
      pooled connection and retains the most recent stack trace to aid debugging
      of abandoned connections. There is significant overhead added by setting this
      to true.
   </td>
</tr>
</table>
<p>
<img src="images/icon_info_sml.gif" alt="Info"/>
If you have enabled removeAbandonedOnMaintenance or removeAbandonedOnBorrow then it is possible that
a connection is reclaimed by the pool because it is considered to be abandoned. This mechanism is triggered
when (getNumIdle() &lt; 2) and (getNumActive() &gt; getMaxTotal() - 3) and removeAbandonedOnBorrow is true;
or after eviction finishes and removeAbandonedOnMaintenance is true. For example, maxTotal=20 and 18 active
connections and 1 idle connection would trigger removeAbandonedOnBorrow, but only the active connections
that aren't used for more then "removeAbandonedTimeout" seconds are removed (default 300 sec). Traversing
a resultset doesn't count as being used. Creating a Statement, PreparedStatement or CallableStatement or
using one of these to execute a query (using one of the execute methods) resets the lastUsed property of
the parent connection.
</p>
<table>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
<tr>
   <td>fastFailValidation</td>
   <td>false</td>
   <td>
      When this property is true, validation fails fast for connections that have
      thrown "fatal" SQLExceptions. Requests to validate disconnected connections
      fail immediately, with no call to the driver's isValid method or attempt to
      execute a validation query.<br/>
      The SQL_STATE codes considered to signal fatal errors are by default the following:
      <ul>
        <li>57P01 (ADMIN SHUTDOWN)</li>
        <li>57P02 (CRASH SHUTDOWN)</li>
        <li>57P03 (CANNOT CONNECT NOW)</li>
        <li>01002 (SQL92 disconnect error)</li>
        <li>JZ0C0 (Sybase disconnect error)</li>
        <li>JZ0C1 (Sybase disconnect error)</li>
        <li>Any SQL_STATE code that starts with "08"</li>
      </ul>
      To override this default set of disconnection codes, set the
      <code>disconnectionSqlCodes</code> property.
   </td>
</tr>
<tr>
   <td>disconnectionSqlCodes</td>
   <td>null</td>
   <td>Comma-delimited list of SQL_STATE codes considered to signal fatal disconnection
       errors. Setting this property has no effect unless
      <code>fastFailValidation</code> is set to <code>true.</code>
   </td>
</tr>
<tr>
   <td>disconnectionIgnoreSqlCodes</td>
   <td>null</td>
   <td>Comma-delimited list of SQL State codes that should be ignored when determining fatal disconnection errors.
       These codes will not trigger a fatal disconnection status, even if they match the usual criteria.
       Setting this property has no effect unless <code>fastFailValidation</code> is set to <code>true.</code>
   </td>
</tr>
<tr>
    <td>jmxName</td>
    <td></td>
    <td>
       Registers the DataSource as JMX MBean under specified name. The name has to conform to the JMX Object Name Syntax (see
       <a href="https://docs.oracle.com/javase/1.5.0/docs/api/javax/management/ObjectName.html">javadoc</a>).
    </td>
</tr>
<tr>
    <td>registerConnectionMBean</td>
    <td>true</td>
    <td>
        Registers Connection JMX MBeans. See <a href="https://issues.apache.org/jira/browse/DBCP-585">DBCP-585</a>).
    </td>
</tr>
</table>

</section>

</body>
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSource.java (L127-157)
```java
     * The default auto-commit state of connections created by this pool.
     */
    private volatile Boolean defaultAutoCommit;

    /**
     * The default read-only state of connections created by this pool.
     */
    private transient Boolean defaultReadOnly;

    /**
     * The default TransactionIsolation state of connections created by this pool.
     */
    private volatile int defaultTransactionIsolation = PoolableConnectionFactory.UNKNOWN_TRANSACTION_ISOLATION;

    private Duration defaultQueryTimeoutDuration;

    /**
     * The default "catalog" of connections created by this pool.
     */
    private volatile String defaultCatalog;

    /**
     * The default "schema" of connections created by this pool.
     */
    private volatile String defaultSchema;

    /**
     * The property that controls if the pooled connections cache some state rather than query the database for current
     * state to improve performance.
     */
    private boolean cacheState = true;
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSource.java (L182-215)
```java
    /**
     * The maximum number of active connections that can be allocated from this pool at the same time, or negative for
     * no limit.
     */
    private int maxTotal = GenericObjectPoolConfig.DEFAULT_MAX_TOTAL;

    /**
     * The maximum number of connections that can remain idle in the pool, without extra ones being destroyed, or
     * negative for no limit. If maxIdle is set too low on heavily loaded systems it is possible you will see
     * connections being closed and almost immediately new connections being opened. This is a result of the active
     * threads momentarily closing connections faster than they are opening them, causing the number of idle connections
     * to rise above maxIdle. The best value for maxIdle for heavily loaded system will vary but the default is a good
     * starting point.
     */
    private int maxIdle = GenericObjectPoolConfig.DEFAULT_MAX_IDLE;

    /**
     * The minimum number of active connections that can remain idle in the pool, without extra ones being created when
     * the evictor runs, or 0 to create none. The pool attempts to ensure that minIdle connections are available when
     * the idle object evictor runs. The value of this property has no effect unless
     * {@link #durationBetweenEvictionRuns} has a positive value.
     */
    private int minIdle = GenericObjectPoolConfig.DEFAULT_MIN_IDLE;

    /**
     * The initial number of connections that are created when the pool is started.
     */
    private int initialSize;

    /**
     * The maximum Duration that the pool will wait (when there are no available connections) for a
     * connection to be returned before throwing an exception, or <= 0 to wait indefinitely.
     */
    private Duration maxWaitDuration = BaseObjectPoolConfig.DEFAULT_MAX_WAIT;
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSource.java (L217-238)
```java
    /**
     * Prepared statement pooling for this pool. When this property is set to {@code true} both PreparedStatements
     * and CallableStatements are pooled.
     */
    private boolean poolPreparedStatements;

    private boolean clearStatementPoolOnReturn;

    /**
     * <p>
     * The maximum number of open statements that can be allocated from the statement pool at the same time, or negative
     * for no limit. Since a connection usually only uses one or two statements at a time, this is mostly used to help
     * detect resource leaks.
     * </p>
     * <p>
     * Note: As of version 1.3, CallableStatements (those produced by {@link Connection#prepareCall}) are pooled along
     * with PreparedStatements (produced by {@link Connection#prepareStatement}) and
     * {@code maxOpenPreparedStatements} limits the total number of prepared or callable statements that may be in
     * use at a given time.
     * </p>
     */
    private int maxOpenPreparedStatements = GenericKeyedObjectPoolConfig.DEFAULT_MAX_TOTAL;
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSource.java (L240-288)
```java
    /**
     * The indication of whether objects will be validated as soon as they have been created by the pool. If the object
     * fails to validate, the borrow operation that triggered the creation will fail.
     */
    private boolean testOnCreate;

    /**
     * The indication of whether objects will be validated before being borrowed from the pool. If the object fails to
     * validate, it will be dropped from the pool, and we will attempt to borrow another.
     */
    private boolean testOnBorrow = true;

    /**
     * The indication of whether objects will be validated before being returned to the pool.
     */
    private boolean testOnReturn;

    /**
     * The number of milliseconds to sleep between runs of the idle object evictor thread. When non-positive, no idle
     * object evictor thread will be run.
     */
    private Duration durationBetweenEvictionRuns = BaseObjectPoolConfig.DEFAULT_DURATION_BETWEEN_EVICTION_RUNS;

    /**
     * The number of objects to examine during each run of the idle object evictor thread (if any).
     */
    private int numTestsPerEvictionRun = BaseObjectPoolConfig.DEFAULT_NUM_TESTS_PER_EVICTION_RUN;

    /**
     * The minimum amount of time an object may sit idle in the pool before it is eligible for eviction by the idle
     * object evictor (if any).
     */
    private Duration minEvictableIdleDuration = BaseObjectPoolConfig.DEFAULT_MIN_EVICTABLE_IDLE_DURATION;

    /**
     * The minimum amount of time a connection may sit idle in the pool before it is eligible for eviction by the idle
     * object evictor, with the extra condition that at least "minIdle" connections remain in the pool. Note that
     * {@code minEvictableIdleTimeMillis} takes precedence over this parameter. See
     * {@link #getSoftMinEvictableIdleDuration()}.
     */
    private Duration softMinEvictableIdleDuration = BaseObjectPoolConfig.DEFAULT_SOFT_MIN_EVICTABLE_IDLE_DURATION;

    private String evictionPolicyClassName = BaseObjectPoolConfig.DEFAULT_EVICTION_POLICY_CLASS_NAME;

    /**
     * The indication of whether objects will be validated by the idle object evictor (if any). If an object fails to
     * validate, it will be dropped from the pool.
     */
    private boolean testWhileIdle;
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSource.java (L322-329)
```java
    /**
     * These SQL statements run once after a Connection is created.
     * <p>
     * This property can be used for example to run ALTER SESSION SET NLS_SORT=XCYECH in an Oracle Database only once
     * after connection creation.
     * </p>
     */
    private volatile List<String> connectionInitSqls;
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSource.java (L331-334)
```java
    /**
     * Controls access to the underlying connection.
     */
    private boolean accessToUnderlyingConnectionAllowed;
```

**File:** src/main/java/org/apache/commons/dbcp2/BasicDataSource.java (L340-342)
```java
    private String jmxName;

    private boolean registerConnectionMBean = true;
```
