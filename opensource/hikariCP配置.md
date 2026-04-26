
---

## 一、数据源 / 驱动连接（必填其一）

| 配置项                                        | 类型         | 默认值  | 选择   | 说明                                                       |                     |
| ------------------------------------------ | ---------- | ---- | ---- | -------------------------------------------------------- | ------------------- |
| `dataSourceClassName`                      | String     | none | 🔒默认 | JDBC DataSource 的完整类名（推荐方式）                              |                     |
| `jdbcUrl`                                  | String     | none | 🔒默认 | JDBC URL，使用 DriverManager 模式（与上互斥）                       |                     |
| `driverClassName`                          | String     | none | 🔒默认 | 驱动类名，仅在 `jdbcUrl` 模式下旧驱动需要                               |                     |
| `dataSourceJNDI`                           | String     | none | 🔒默认 | 通过 JNDI 查找 DataSource                                    |                     |
| `dataSource`                               | DataSource | none | 🔒默认 | 直接注入 DataSource 实例（**仅编程方式**）                            |                     |
| `dataSource.*` / `addDataSourceProperty()` | Properties | —    | 🔒默认 | 透传给底层 DataSource 的属性（如 `dataSource.cachePrepStmts=true`） | [1](#0-0) [2](#0-1) |

---

## 二、认证 / 凭证

| 配置项                            | 类型                        | 默认值  | 选择   | 说明                                               |                               |
| ------------------------------ | ------------------------- | ---- | ---- | ------------------------------------------------ | ----------------------------- |
| `username`                     | String                    | none | 🔒默认 | 数据库用户名                                           |                               |
| `password`                     | String                    | none | 🔒默认 | 数据库密码                                            |                               |
| `credentials`                  | Credentials               | none | 🔒默认 | 原子性同时设置用户名+密码（**仅编程/JMX**）                       |                               |
| `credentialsProviderClassName` | String                    | none | 🔒默认 | 实现 `HikariCredentialsProvider` 接口的类名，用于运行时动态获取凭证 |                               |
| `credentialsProvider`          | HikariCredentialsProvider | none | 🔒默认 | 直接注入凭证提供者实例（**仅编程方式**）                           | [3](#0-2) [4](#0-3) [5](#0-4) |

---

## 三、连接池大小

| 配置项               | 类型  | 默认值              | 选择   | 运行时可变 | 说明                             |           |
| ----------------- | --- | ---------------- | ---- | ----- | ------------------------------ | --------- |
| `maximumPoolSize` | int | 10               | 🔄动态 | 是     | 池的最大连接数（含空闲+使用中）               |           |
| `minimumIdle`     | int | =maximumPoolSize | 🔄动态 | 是     | 池中维持的最小空闲连接数；建议不设置，让池作为固定大小池运行 | [6](#0-5) |

---

## 四、超时与生命周期

| 配置项                         | 类型        | 默认值     | 选择      | 运行时可变 | 说明                                                           | 最小值     |                     |
| --------------------------- | --------- | ------- | ------- | ----- | ------------------------------------------------------------ | ------- | ------------------- |
| `connectionTimeout`         | long (ms) | 30000   | ✅保持2000 | 是     | 客户端等待连接的最大时长，超时抛 `SQLException`                              | 250ms   |                     |
| `validationTimeout`         | long (ms) | 5000    | ✅保持500  | 是     | 验证连接存活的最大时长，须小于 `connectionTimeout`                          | 250ms   |                     |
| `idleTimeout`               | long (ms) | 600000  | ✅保持600秒 | 是     | 空闲连接在池中的最大存活时长（仅 `minimumIdle < maximumPoolSize` 时生效），0=永不移除 | 10000ms |                     |
| `maxLifetime`               | long (ms) | 1800000 | ✅保持30分钟 | 是     | 连接的最大生命周期，0=无限制；**强烈建议设置，且比数据库/基础设施的连接超时短几秒**                | 30000ms |                     |
| `keepaliveTime`             | long (ms) | 120000  | ✅保持300秒 | 否     | 对空闲连接发送保活 ping 的间隔，须小于 `maxLifetime`，0=禁用                    | 30000ms |                     |
| `leakDetectionThreshold`    | long (ms) | 0       | ✅保持默认关闭 | 是     | 【实质是给每个连接开一个定时打印任务，时间到前结束就不打了】连接借出超过此时长则记录泄漏警告，0=禁用          | 2000ms  |                     |
| `initializationFailTimeout` | long (s)  | 1       | ✅保持1秒   | 否     | 池初始化时获取首个连接的超时；>0=阻塞等待；0=尝试验证但失败时仍启动；<0=跳过初始化直接启动            | —       | [7](#0-6) [8](#0-7) |

---

## 五、连接行为

| 配置项                      | 类型      | 默认值            | 选择                      | 运行时可变             | 说明                                                          |                      |
| ------------------------ | ------- | -------------- | ----------------------- | ----------------- | ----------------------------------------------------------- | -------------------- |
| `autoCommit`             | boolean | true           | ✅保持开启                   | 否                 | 连接的默认自动提交行为                                                 |                      |
| `readOnly`               | boolean | false          | 🔄是否需要                  | 否                 | 连接是否以只读模式返回                                                 |                      |
| `transactionIsolation`   | String  | driver default | 🔒默认                    | 否                 | 默认事务隔离级别，取 `Connection` 类常量名，如 `TRANSACTION_READ_COMMITTED` |                      |
| `catalog`                | String  | driver default | 🔒默认                    | **是**（建议仅在池挂起后修改） | 连接的默认 catalog                                               |                      |
| `schema`                 | String  | driver default | 🔒默认                    | 否                 | 连接的默认 schema                                                |                      |
| `connectionInitSql`      | String  | none           | 🔒默认【不只是用来检测，还用来调SET语句】 | 否                 | 每个新连接创建后、加入池前执行的 SQL；执行失败视为连接失败                             |                      |
| `connectionTestQuery`    | String  | none           | 可替换SELECT 1             | 否                 | 连接存活验证 SQL（仅供不支持 JDBC4 `isValid()` 的旧驱动使用）                  |                      |
| `isolateInternalQueries` | boolean | false          | 🔒默认                    | 否                 | 是否将内部查询（如存活检测）包裹在独立事务中（仅 `autoCommit=false` 时有效）            | [9](#0-8) [10](#0-9) |
- 物理连接的真正初始化逻辑在 PoolBase.newConnection() 与 setupConnection()：
	- 设置 networkTimeout、默认只读/自动提交/隔离级别、catalog/schema，执行 connectionInitSql，并检查 JDBC4 isValid() 或 connectionTestQuery 支持。
	- 简化路径是：HikariDataSource ctor -> HikariPool ctor -> checkFailFast -> createPoolEntry -> newConnection -> setupConnection。

---

## 六、监控与指标

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `metricRegistry` | Object | none | Codahale `MetricRegistry`、Dropwizard metrics5 `MetricRegistry` 或 Micrometer `MeterRegistry` 实例（**仅编程方式**，也支持 JNDI 字符串） |
| `metricsTrackerFactory` | MetricsTrackerFactory | none | 自定义指标追踪工厂（**仅编程方式**，与 `metricRegistry` 互斥） |
| `healthCheckRegistry` | Object | none | Codahale `HealthCheckRegistry` 实例（**仅编程方式**） |
| `healthCheckProperties` | Properties | — | 传递给健康检查的附加属性（通过 `addHealthCheckProperty()` 添加） | [11](#0-10) [12](#0-11) 

---

## 七、JMX 管理

| 配置项                   | 类型      | 默认值   | 说明                                                   |             |
| --------------------- | ------- | ----- | ---------------------------------------------------- | ----------- |
| `registerMbeans`      | boolean | false | 是否向 JMX 注册 `HikariConfigMXBean` 和 `HikariPoolMXBean` |             |
| `allowPoolSuspension` | boolean | false | 是否允许通过 JMX 挂起/恢复连接池（有性能开销，仅用于故障转移场景）                 | [13](#0-12) |

---

## 八、线程与执行器

| 配置项                 | 类型                       | 默认值        | 选择    | 说明                                                           |             |
| ------------------- | ------------------------ | ---------- | ----- | ------------------------------------------------------------ | ----------- |
| `threadFactory`     | ThreadFactory            | none（内部默认） | 🔒默认  | 创建池内所有线程的工厂（**仅编程方式**，用于受限容器环境）                              |             |
| `scheduledExecutor` | ScheduledExecutorService | none（内部默认） | ✅保持共用 | 用于内部定时任务的调度器（**仅编程方式**），建议设置 `setRemoveOnCancelPolicy(true)` | [14](#0-13) |

---

## 九、异常处理

| 配置项                          | 类型                   | 默认值  | 说明                                                                                   |                         |
| ---------------------------- | -------------------- | ---- | ------------------------------------------------------------------------------------ | ----------------------- |
| `exceptionOverrideClassName` | String               | none | 实现 `SQLExceptionOverride` 接口的类名，用于自定义连接驱逐逻辑                                          |                         |
| `exceptionOverride`          | SQLExceptionOverride | none | 直接注入实例（**仅编程方式**），`adjudicate()` 返回 `CONTINUE_EVICT` / `DO_NOT_EVICT` / `MUST_EVICT` | [15](#0-14) [16](#0-15) |

---

## 十、池标识

| 配置项        | 类型     | 默认值                  | 说明                                 |             |
| ---------- | ------ | -------------------- | ---------------------------------- | ----------- |
| `poolName` | String | 自动生成（`HikariPool-N`） | 连接池名称，用于日志和 JMX 标识；使用 JMX 时不能含 `:` | [17](#0-16) |

---

## 十一、配置文件加载（系统属性）

| 系统属性                         | 说明                                   |             |
| ---------------------------- | ------------------------------------ | ----------- |
| `hikaricp.configurationFile` | 指定 `.properties` 配置文件路径，使用无参构造器时自动加载 | [18](#0-17) |

---

## 十二、隐藏系统属性（Secret Properties，不受官方支持）

> 官方明确声明：这些属性随时可能消失，不要开 issue。

| 系统属性 | 说明 |
|---|---|
| `com.zaxxer.hikari.blockUntilFilled` | 为 `true` 且 `initializationFailTimeout > 1` 时，启动时阻塞直到池完全填满 |
| `com.zaxxer.hikari.enableRequestBoundaries` | 为 `true` 时，在连接获取/归还时调用 `Connection.beginRequest()` / `endRequest()` |
| `com.zaxxer.hikari.housekeeping.period` | 控制内部 housekeeping 线程的执行频率（ms），**不要修改** |
| `com.zaxxer.hikari.legacy.supportUserPassDataSourceOverride` | 为 `true` 时支持旧版 `getUsername()/getPassword()` 覆盖行为（新版推荐用 `getCredentials()`） |
| `com.zaxxer.hikari.useWeakReferences` | 为 `true` 时强制 `ConcurrentBag` 使用 `WeakReference`，避免 Tomcat 热部署警告 |
| `com.zaxxer.hikari.timeoutMs.floor` | 超时时间的最小下限（ms），默认 250，影响 `connectionTimeout` 和 `validationTimeout` 的校验 | [19](#0-18) [20](#0-19) 

---

## 运行时可变属性汇总（通过 `HikariConfigMXBean` / JMX）

以下属性声明为 `volatile`，可在池运行期间动态修改：

`catalog` · `connectionTimeout` · `validationTimeout` · `idleTimeout` · `leakDetectionThreshold` · `maxLifetime` · `maximumPoolSize` · `minimumIdle` · `username` · `password` · `credentials` [21](#0-20) [22](#0-21)

### Citations

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L50-70)
```java
   private static final long CONNECTION_TIMEOUT = SECONDS.toMillis(30);
   private static final long VALIDATION_TIMEOUT = SECONDS.toMillis(5);
   private static final long SOFT_TIMEOUT_FLOOR = Long.getLong("com.zaxxer.hikari.timeoutMs.floor", 250L);
   private static final long IDLE_TIMEOUT = MINUTES.toMillis(10);
   private static final long MAX_LIFETIME = MINUTES.toMillis(30);
   private static final long DEFAULT_KEEPALIVE_TIME = MINUTES.toMillis(2);
   private static final int DEFAULT_POOL_SIZE = 10;

   private static boolean unitTest = false;

   // Properties changeable at runtime through the HikariConfigMXBean
   //
   private volatile String catalog;
   private volatile long connectionTimeout;
   private volatile long validationTimeout;
   private volatile long idleTimeout;
   private volatile long leakDetectionThreshold;
   private volatile long maxLifetime;
   private volatile int maxPoolSize;
   private volatile int minIdle;
   private final AtomicReference<Credentials> credentials = new AtomicReference<>(Credentials.of(null, null));
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L72-84)
```java
   // Properties NOT changeable at runtime
   //
   private long initializationFailTimeout;
   private String connectionInitSql;
   private String connectionTestQuery;
   private String credentialsProviderClassName;
   private String dataSourceClassName;
   private String dataSourceJndiName;
   private String driverClassName;
   private String exceptionOverrideClassName;
   private SQLExceptionOverride exceptionOverride;
   private String jdbcUrl;
   private String poolName;
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L87-91)
```java
   private boolean isAutoCommit;
   private boolean isReadOnly;
   private boolean isIsolateInternalQueries;
   private boolean isRegisterMbeans;
   private boolean isAllowPoolSuspension;
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L95-96)
```java
   private ThreadFactory threadFactory;
   private ScheduledExecutorService scheduledExecutor;
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L97-100)
```java
   private MetricsTrackerFactory metricsTrackerFactory;
   private Object metricRegistry;
   private Object healthCheckRegistry;
   private Properties healthCheckProperties;
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L130-133)
```java
      var systemProp = System.getProperty("hikaricp.configurationFile");
      if (systemProp != null) {
         loadProperties(systemProp);
      }
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L672-690)
```java
   public void setMetricRegistry(Object metricRegistry)
   {
      if (metricsTrackerFactory != null) {
         throw new IllegalStateException("cannot use setMetricRegistry() and setMetricsTrackerFactory() together");
      }

      if (metricRegistry != null) {
         metricRegistry = getObjectOrPerformJndiLookup(metricRegistry);

         if (!safeIsAssignableFrom(metricRegistry, "com.codahale.metrics.MetricRegistry")
             && !(safeIsAssignableFrom(metricRegistry, "io.dropwizard.metrics5.MetricRegistry"))
             && !(safeIsAssignableFrom(metricRegistry, "io.micrometer.core.instrument.MeterRegistry"))) {
            throw new IllegalArgumentException("Class must be instance of com.codahale.metrics.MetricRegistry, " +
               "io.dropwizard.metrics5.MetricRegistry, or io.micrometer.core.instrument.MeterRegistry");
         }
      }

      this.metricRegistry = metricRegistry;
   }
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L876-921)
```java
   public String getCredentialsProviderClassName()
   {
      return credentialsProviderClassName;
   }

   /**
    * Set the class name of the {@link HikariCredentialsProvider} that will be used to get credentials at runtime. Use this method
    * or provide a {@link HikariCredentialsProvider} instance via the {@link #setCredentialsProvider(HikariCredentialsProvider)} method.
    *
    * @param credentialsProviderClassName the class name of the credentials provider
    * @see HikariCredentialsProvider
    */
   public void setCredentialsProviderClassName(String credentialsProviderClassName) {
      checkIfSealed();

      try {
         this.credentialsProvider = createInstance(credentialsProviderClassName, HikariCredentialsProvider.class);
         this.exceptionOverrideClassName = credentialsProviderClassName;
      }
      catch (Exception e) {
         throw new RuntimeException("Failed to instantiate class " + credentialsProviderClassName, e);
      }
   }

   /**
    * Get the {@link HikariCredentialsProvider} instance created by {@link #setCredentialsProviderClassName(String)} or specified by
    * {@link #setCredentialsProvider(HikariCredentialsProvider)}.
    *
    * @return the HikariCredentialsProvider instance, or null
    * @see HikariCredentialsProvider
    */
   public HikariCredentialsProvider getCredentialsProvider() {
      return credentialsProvider;
   }

   /**
    * Set a user supplied {@link HikariCredentialsProvider} instance. If this method is used, then the {@link #setCredentialsProviderClassName(String)}
    * method should not be used. The {@link HikariCredentialsProvider} instance will be used to get credentials at runtime.
    *
    * @param credentialsProvider a user supplied HikariCredentialsProvider instance
    * @see HikariCredentialsProvider
    */
   public void setCredentialsProvider(HikariCredentialsProvider credentialsProvider) {
      checkIfSealed();
      this.credentialsProvider = credentialsProvider;
   }
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L929-974)
```java
   public String getExceptionOverrideClassName()
   {
      return this.exceptionOverrideClassName;
   }

   /**
    * Set the user supplied SQLExceptionOverride class name.
    *
    * @param exceptionOverrideClassName the user supplied SQLExceptionOverride class name
    * @see SQLExceptionOverride
    */
   public void setExceptionOverrideClassName(String exceptionOverrideClassName)
   {
      checkIfSealed();

      try {
         this.exceptionOverride = createInstance(exceptionOverrideClassName, SQLExceptionOverride.class);
         this.exceptionOverrideClassName = exceptionOverrideClassName;
      }
      catch (Exception e) {
         throw new RuntimeException("Failed to instantiate class " + exceptionOverrideClassName, e);
      }
   }

   /**
    * Get the SQLExceptionOverride instance created by {@link #setExceptionOverrideClassName(String)} or specified by
    * {@link #setExceptionOverride(SQLExceptionOverride)}.
    *
    * @return the SQLExceptionOverride instance, or null
    * @see SQLExceptionOverride
    */
   public SQLExceptionOverride getExceptionOverride()
   {
      return this.exceptionOverride;
   }

   /**
    * Set the user supplied SQLExceptionOverride instance.
    *
    * @param exceptionOverride the user supplied SQLExceptionOverride instance
    * @see SQLExceptionOverride
    */
   public void setExceptionOverride(SQLExceptionOverride exceptionOverride) {
      checkIfSealed();
      this.exceptionOverride = exceptionOverride;
   }
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfig.java (L1101-1151)
```java
   private void validateNumerics()
   {
      if (maxLifetime != 0 && maxLifetime < SECONDS.toMillis(30)) {
         LOGGER.warn("{} - maxLifetime is less than 30000ms, setting to default {}ms.", poolName, MAX_LIFETIME);
         maxLifetime = MAX_LIFETIME;
      }

      // keepalive time must larger than 30 seconds
      if (keepaliveTime != 0 && keepaliveTime < SECONDS.toMillis(30)) {
         LOGGER.warn("{} - keepaliveTime is less than 30000ms, disabling it.", poolName);
         keepaliveTime = 0L;
      }

      // keepalive time must be less than maxLifetime (if maxLifetime is enabled)
      if (keepaliveTime != 0 && maxLifetime != 0 && keepaliveTime >= maxLifetime) {
         LOGGER.warn("{} - keepaliveTime is greater than or equal to maxLifetime, disabling it.", poolName);
         keepaliveTime = 0L;
      }

      if (leakDetectionThreshold > 0 && !unitTest) {
         if (leakDetectionThreshold < SECONDS.toMillis(2) || (leakDetectionThreshold > maxLifetime && maxLifetime > 0)) {
            LOGGER.warn("{} - leakDetectionThreshold is less than 2000ms or more than maxLifetime, disabling it.", poolName);
            leakDetectionThreshold = 0;
         }
      }

      if (connectionTimeout < SOFT_TIMEOUT_FLOOR) {
         LOGGER.warn("{} - connectionTimeout is less than {}ms, setting to {}ms.", poolName, SOFT_TIMEOUT_FLOOR, CONNECTION_TIMEOUT);
         connectionTimeout = CONNECTION_TIMEOUT;
      }

      if (validationTimeout < SOFT_TIMEOUT_FLOOR) {
         LOGGER.warn("{} - validationTimeout is less than {}ms, setting to {}ms.", poolName, SOFT_TIMEOUT_FLOOR, VALIDATION_TIMEOUT);
         validationTimeout = VALIDATION_TIMEOUT;
      }

      if (minIdle < 0 || minIdle > maxPoolSize) {
         minIdle = maxPoolSize;
      }

      if (idleTimeout + SECONDS.toMillis(1) > maxLifetime && maxLifetime > 0 && minIdle < maxPoolSize) {
         LOGGER.warn("{} - idleTimeout is close to or more than maxLifetime, disabling it.", poolName);
         idleTimeout = 0;
      }
      else if (idleTimeout != 0 && idleTimeout < SECONDS.toMillis(10) && minIdle < maxPoolSize) {
         LOGGER.warn("{} - idleTimeout is less than 10000ms, setting to default {}ms.", poolName, IDLE_TIMEOUT);
         idleTimeout = IDLE_TIMEOUT;
      }
      else  if (idleTimeout != IDLE_TIMEOUT && idleTimeout != 0 && minIdle == maxPoolSize) {
         LOGGER.warn("{} - idleTimeout has been set but has no effect because the pool is operating as a fixed size pool.", poolName);
      }
```

**File:** src/main/java/com/zaxxer/hikari/util/PropertyElf.java (L52-54)
```java
         if (target instanceof HikariConfig && keyName.startsWith("dataSource.")) {
            ((HikariConfig) target).addDataSourceProperty(keyName.substring("dataSource.".length()), value);
         }
```

**File:** src/main/java/com/zaxxer/hikari/HikariConfigMXBean.java (L26-203)
```java
public interface HikariConfigMXBean
{
   /**
    * Get the maximum number of milliseconds that a client will wait for a connection from the pool. If this
    * time is exceeded without a connection becoming available, a SQLException will be thrown from
    * {@link javax.sql.DataSource#getConnection()}.
    *
    * @return the connection timeout in milliseconds
    */
   long getConnectionTimeout();

   /**
    * Set the maximum number of milliseconds that a client will wait for a connection from the pool. If this
    * time is exceeded without a connection becoming available, a SQLException will be thrown from
    * {@link javax.sql.DataSource#getConnection()}.
    *
    * @param connectionTimeoutMs the connection timeout in milliseconds
    */
   void setConnectionTimeout(long connectionTimeoutMs);

   /**
    * Get the maximum number of milliseconds that the pool will wait for a connection to be validated as
    * alive.
    *
    * @return the validation timeout in milliseconds
    */
   long getValidationTimeout();

   /**
    * Sets the maximum number of milliseconds that the pool will wait for a connection to be validated as
    * alive.
    *
    * @param validationTimeoutMs the validation timeout in milliseconds
    */
   void setValidationTimeout(long validationTimeoutMs);

   /**
    * This property controls the maximum amount of time (in milliseconds) that a connection is allowed to sit
    * idle in the pool. Whether a connection is retired as idle or not is subject to a maximum variation of +30
    * seconds, and average variation of +15 seconds. A connection will never be retired as idle before this timeout.
    * A value of 0 means that idle connections are never removed from the pool.
    *
    * @return the idle timeout in milliseconds
    */
   long getIdleTimeout();

   /**
    * This property controls the maximum amount of time (in milliseconds) that a connection is allowed to sit
    * idle in the pool. Whether a connection is retired as idle or not is subject to a maximum variation of +30
    * seconds, and average variation of +15 seconds. A connection will never be retired as idle before this timeout.
    * A value of 0 means that idle connections are never removed from the pool.
    *
    * @param idleTimeoutMs the idle timeout in milliseconds
    */
   void setIdleTimeout(long idleTimeoutMs);

   /**
    * This property controls the amount of time that a connection can be out of the pool before a message is
    * logged indicating a possible connection leak. A value of 0 means leak detection is disabled.
    *
    * @return the connection leak detection threshold in milliseconds
    */
   long getLeakDetectionThreshold();

   /**
    * This property controls the amount of time that a connection can be out of the pool before a message is
    * logged indicating a possible connection leak. A value of 0 means leak detection is disabled.
    *
    * @param leakDetectionThresholdMs the connection leak detection threshold in milliseconds
    */
   void setLeakDetectionThreshold(long leakDetectionThresholdMs);

   /**
    * This property controls the maximum lifetime of a connection in the pool. When a connection reaches this
    * timeout, even if recently used, it will be retired from the pool. An in-use connection will never be
    * retired, only when it is idle will it be removed.
    *
    * @return the maximum connection lifetime in milliseconds
    */
   long getMaxLifetime();

   /**
    * This property controls the maximum lifetime of a connection in the pool. When a connection reaches this
    * timeout, even if recently used, it will be retired from the pool. An in-use connection will never be
    * retired, only when it is idle will it be removed.
    *
    * @param maxLifetimeMs the maximum connection lifetime in milliseconds
    */
   void setMaxLifetime(long maxLifetimeMs);

   /**
    * The property controls the minimum number of idle connections that HikariCP tries to maintain in the pool,
    * including both idle and in-use connections. If the idle connections dip below this value, HikariCP will
    * make a best effort to restore them quickly and efficiently.
    *
    * @return the minimum number of connections in the pool
    */
   int getMinimumIdle();

   /**
    * The property controls the minimum number of idle connections that HikariCP tries to maintain in the pool,
    * including both idle and in-use connections. If the idle connections dip below this value, HikariCP will
    * make a best effort to restore them quickly and efficiently.
    *
    * @param minIdle the minimum number of idle connections in the pool to maintain
    */
   void setMinimumIdle(int minIdle);

   /**
    * The property controls the maximum number of connections that HikariCP will keep in the pool,
    * including both idle and in-use connections.
    *
    * @return the maximum number of connections in the pool
    */
   int getMaximumPoolSize();

   /**
    * The property controls the maximum size that the pool is allowed to reach, including both idle and in-use
    * connections. Basically this value will determine the maximum number of actual connections to the database
    * backend.
    * <p>
    * When the pool reaches this size, and no idle connections are available, calls to getConnection() will
    * block for up to connectionTimeout milliseconds before timing out.
    *
    * @param maxPoolSize the maximum number of connections in the pool
    */
   void setMaximumPoolSize(int maxPoolSize);

   /**
    * Set the password used for authentication. Changing this at runtime will apply to new connections only.
    * Altering this at runtime only works for DataSource-based connections, not Driver-class or JDBC URL-based
    * connections.
    *
    * @param password the database password
    */
   void setPassword(String password);

   /**
    * Set the username used for authentication. Changing this at runtime will apply to new connections only.
    * Altering this at runtime only works for DataSource-based connections, not Driver-class or JDBC URL-based
    * connections.
    *
    * @param username the database username
    */
   void setUsername(String username);

   /**
    * Set the username and password used for authentication. Changing this at runtime will apply to new
    * connections only. Altering this at runtime only works for DataSource-based connections, not Driver-class
    * or JDBC URL-based connections.
    *
    * @param credentials the database username and password pair
    */
   void setCredentials(Credentials credentials);

   /**
    * The name of the connection pool.
    *
    * @return the name of the connection pool
    */
   String getPoolName();

   /**
    * Get the default catalog name to be set on connections.
    *
    * @return the default catalog name
    */
   String getCatalog();

   /**
    * Set the default catalog name to be set on connections.
    * <p>
    * WARNING: THIS VALUE SHOULD ONLY BE CHANGED WHILE THE POOL IS SUSPENDED, AFTER CONNECTIONS HAVE BEEN EVICTED.
    *
    * @param catalog the catalog name, or null
    */
   void setCatalog(String catalog);
}
```

**File:** README.md (L437-444)
```markdown
| Property                                      | Description                                                                                                                                                                                                                                       |
|:----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ``com.zaxxer.hikari.blockUntilFilled``        | When this property is set ``true`` *and* ``initializationFailTimeout`` is greater than 1, the pool will block during start until completely filled.                                                                                               |
| ``com.zaxxer.hikari.enableRequestBoundaries`` | When this property is set ``true``, HikariCP will bracket connection acquisition and return with calls to ``Connection.beginRequest()`` and ``Connection.endRequest()``.                                                                          |
| ``com.zaxxer.hikari.housekeeping.period``     | This property controls the frequency of the housekeeping thread, represented in milliseconds. Really, don't mess with this.                                                                                                                       |
| ``com.zaxxer.hikari.legacy.supportUserPassDataSourceOverride`` | When this property is set ``true``, HikariCP will support the legacy behavior of overriding the ``getUsername()/getPassword()`` methods on *HikariDataSource*. Preferred method is overriding ``getCredentials()``.             |
| ``com.zaxxer.hikari.useWeakReferences``       | When this property is set ``true`` it will force HikariCP to use ``WeakReference`` objects in the ``ConcurrentBag`` internal collection ThreadLocals and prevent the use of our ``FastList`` class, all to avoid TomCat warnings during redeploy. |

```
