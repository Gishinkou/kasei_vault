
37 个配置项，14 个字符串项，共 51 项
PROP_DEFAULTAUTOCOMMIT,  
PROP_DEFAULTREADONLY,  
PROP_DEFAULTTRANSACTIONISOLATION,  
PROP_DEFAULTCATALOG,  
PROP_DRIVERCLASSNAME,  
PROP_MAXACTIVE,  
PROP_MAXIDLE,  
PROP_MINIDLE,  
PROP_INITIALSIZE,  
PROP_MAXWAIT,  
PROP_TESTONBORROW,  
PROP_TESTONRETURN,  
PROP_TIMEBETWEENEVICTIONRUNSMILLIS,  
PROP_NUMTESTSPEREVICTIONRUN,  
PROP_MINEVICTABLEIDLETIMEMILLIS,  
PROP_MAXEVICTABLEIDLETIMEMILLIS,  
PROP_TESTWHILEIDLE,  
PROP_PASSWORD,  
PROP_FILTERS,  
PROP_URL,  
PROP_USERNAME,  
PROP_VALIDATIONQUERY,  
PROP_VALIDATIONQUERY_TIMEOUT,  
PROP_INITCONNECTIONSQLS,  
PROP_ACCESSTOUNDERLYINGCONNECTIONALLOWED,  
PROP_REMOVEABANDONED,  
PROP_REMOVEABANDONEDTIMEOUT,  
PROP_LOGABANDONED,  
PROP_POOLPREPAREDSTATEMENTS,  
PROP_MAXOPENPREPAREDSTATEMENTS,  
PROP_CONNECTIONPROPERTIES,  
PROP_EXCEPTION_SORTER,  
PROP_EXCEPTION_SORTER_CLASS_NAME,  
PROP_INIT,  
PROP_NAME,  
PROP_CONNECT_TIMEOUT,  
PROP_SOCKET_TIMEOUT,
"druid.timeBetweenLogStatsMillis",  
"druid.stat.sql.MaxSize",  
"druid.clearFiltersEnable",  
"druid.resetStatEnable", //  
"druid.notFullTimeoutRetryCount", //  
"druid.maxWaitThreadCount", //  
"druid.failFast", //  
"druid.phyTimeoutMillis", //  
"druid.wall.tenantColumn", //  
"druid.wall.updateAllow", //  
"druid.wall.deleteAllow", //  
"druid.wall.insertAllow", //  
"druid.wall.selelctAllow", //  
"druid.wall.multiStatementAllow", //

|                                           |                 |                                                                                                                                                                                                                  |                                                                                                                               |
| ----------------------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| connectProperties✅                        | {}              | map方式放入自定义的key和value，在Filter等地方可以获取该信息进行相应逻辑控制                                                                                                                                                                   | public void com.alibaba.druid.pool.DruidDataSource.setConnectProperties(java.util.Properties)                                 |
| connectionProperties                      | null            | 字符串方式放入自定义的key和value，键值对用分号隔开，比如“a=b;c=d”，传入空白字符串表示清空属性，实际拆分字符串后赋值给connectProperties，在Filter等地方可以获取该信息进行相应逻辑控制                                                                                                   | public void com.alibaba.druid.pool.DruidAbstractDataSource.setConnectionProperties(java.lang.String)                          |
| connectTimeout                            | 0               | 新增的控制创建连接时的socket连接最大等待超时，单位是毫秒，默认0表示永远等待，工作原理是在创建连接时将该值设置到对应数据库驱动的属性信息中由其JDBC驱动进行控制                                                                                                                             | public void com.alibaba.druid.pool.DruidAbstractDataSource.setConnectTimeout(int)                                             |
| connectionInitSqls                        | []              | 数组方式定义物理连接初始化的时候执行的1到多条sql语句，比如连接MySQL数据库使用低版本驱动的情况下，想使用utf8mb4,则可以配置sql为： set NAMES 'utf8mb4'                                                                                                                   | public void com.alibaba.druid.pool.DruidAbstractDataSource.setConnectionInitSqls(java.util.Collection)                        |
| createScheduler                           | null            | 可以使用定时线程池方式异步创建连接，比起默认的单线程创建连接方式，经实际验证这种更可靠                                                                                                                                                                      | public void com.alibaba.druid.pool.DruidAbstractDataSource.setCreateScheduler(java.util.concurrent.ScheduledExecutorService)  |
| dbType                                    | null            | 对于不是Druid自动适配支持的db类型，可以强制指定db类型，字符串值来自com.alibaba.druid.DbType的枚举名                                                                                                                                               | public void com.alibaba.druid.pool.DruidAbstractDataSource.setDbType(java.lang.String)                                        |
| destroyScheduler                          | null            | 可以使用定时线程池方式异步创建连接，比起默认的单线程创建连接方式，经实际验证这种更可靠                                                                                                                                                                      | public void com.alibaba.druid.pool.DruidAbstractDataSource.setDestroyScheduler(java.util.concurrent.ScheduledExecutorService) |
| driverClassName                           | 根据url自动识别       | 这一项可配可不配，如果不配置druid会根据url自动识别dbType，然后选择相应的driverClassName                                                                                                                                                       | com.alibaba.druid.pool.DruidAbstractDataSource.setDriverClassName(String)                                                     |
| exceptionSorter                           | null            | 当数据库抛出一些不可恢复的异常时，抛弃连接                                                                                                                                                                                            | public void com.alibaba.druid.pool.DruidAbstractDataSource.setExceptionSorter(com.alibaba.druid.pool.ExceptionSorter)         |
| failFast                                  | false           | null                                                                                                                                                                                                             | public void com.alibaba.druid.pool.DruidAbstractDataSource.setFailFast(boolean)                                               |
| filters                                   |                 | 属性类型是逗号隔开的字符串，通过别名的方式配置扩展插件，插件别名列表请参考druid jar包中的 /META-INF/druid-filter.properties,常用的插件有：  <br>监控统计用的filter:stat  <br>日志用的filter:log4j  <br>防御sql注入的filter:wall  <br>防御sql注入的filter:wall                       | com.alibaba.druid.pool.DruidAbstractDataSource.setFilters(String)                                                             |
| initialSize                               | 0               | 初始化数据源时建立物理连接的个数。初始化发生在显示调用init方法，或者第一次getConnection时                                                                                                                                                            | public void com.alibaba.druid.pool.DruidAbstractDataSource.setInitialSize(int)                                                |
| keepAlive                                 | false           | 连接池中的minIdle数量以内的连接，空闲时间超过minEvictableIdleTimeMillis，则会执行keepAlive操作。实际项目中建议配置成true                                                                                                                              | public void com.alibaba.druid.pool.DruidDataSource.setKeepAlive(boolean)                                                      |
| keepAliveBetweenTimeMillis                | 120000          | null                                                                                                                                                                                                             | public void com.alibaba.druid.pool.DruidAbstractDataSource.setKeepAliveBetweenTimeMillis(long)                                |
| logAbandoned                              | false           | 在开启removeAbandoned为true的情况，可以开启该设置，druid在销毁未及时关闭的连接时，则会输出日志信息，便于定位连接泄露问题                                                                                                                                         | public void com.alibaba.druid.pool.DruidAbstractDataSource.setLogAbandoned(boolean)                                           |
| loginTimeout                              |                 | 单位是秒，底层调用DriverManager全局静态方法                                                                                                                                                                                     | java.sql.DriverManager.setLoginTimeout(int)                                                                                   |
| maxActive                                 | 8               | 连接池最大活跃连接数量，当连接数量达到该值时，再获取新连接时，将处于等待状态，直到有连接被释放，才能借用成功                                                                                                                                                           | public void com.alibaba.druid.pool.DruidDataSource.setMaxActive(int)                                                          |
| maxEvictableIdleTimeMillis                | 25200000        | null                                                                                                                                                                                                             | public void com.alibaba.druid.pool.DruidAbstractDataSource.setMaxEvictableIdleTimeMillis(long)                                |
| maxIdle                                   | 8               | 已经彻底废弃，配置了也没效果，以maxActive为准                                                                                                                                                                                      | public void com.alibaba.druid.pool.DruidAbstractDataSource.setMaxIdle(int)                                                    |
| maxOpenPreparedStatements                 | 10              | null                                                                                                                                                                                                             | public void com.alibaba.druid.pool.DruidAbstractDataSource.setMaxOpenPreparedStatements(int)                                  |
| maxPoolPreparedStatementPerConnectionSize | 10              | 要启用PSCache，必须配置大于0，当大于0时，poolPreparedStatements自动触发修改为true。在Druid中，不会存在Oracle下PSCache占用内存过多的问题，可以把这个数值配置大一些，比如说100                                                                                               | public void com.alibaba.druid.pool.DruidAbstractDataSource.setMaxPoolPreparedStatementPerConnectionSize(int)                  |
| maxWait                                   | -1              | 获取连接时最大等待时间，单位毫秒。配置了maxWait之后，缺省启用公平锁，并发效率会有所下降，如果需要可以通过配置useUnfairLock属性为true使用非公平锁。                                                                                                                            | public void com.alibaba.druid.pool.DruidAbstractDataSource.setMaxWait(long)                                                   |
| minEvictableIdleTimeMillis                | 1800000         | 连接保持空闲而不被驱逐的最小时间                                                                                                                                                                                                 | public void com.alibaba.druid.pool.DruidAbstractDataSource.setMinEvictableIdleTimeMillis(long)                                |
| minIdle                                   | 0               | 连接池最小空闲数量                                                                                                                                                                                                        | public void com.alibaba.druid.pool.DruidAbstractDataSource.setMinIdle(int)                                                    |
| name                                      | DataSource-**** | 配置这个属性的意义在于，如果存在多个数据源，监控的时候可以通过名字来区分开来。如果没有配置，将会生成一个名字，格式是："DataSource-" + System.identityHashCode(this). 另外配置此属性至少在1.0.5版本中是不起作用的，强行设置name会出错。[详情-点此处](http://blog.csdn.net/lanmo555/article/details/41248763)。 | public void com.alibaba.druid.pool.DruidAbstractDataSource.setName(java.lang.String)                                          |
| numTestsPerEvictionRun                    | 3               | 不再使用，已经彻底废弃，一个DruidDataSource只支持一个EvictionRun                                                                                                                                                                    | public void com.alibaba.druid.pool.DruidAbstractDataSource.setNumTestsPerEvictionRun(int)                                     |
| password                                  | null            | 连接数据库的密码。如果你不希望密码直接写在配置文件中，可以使用passwordCallback进行配置，或者使用ConfigFilter。[详细看这里](https://github.com/alibaba/druid/wiki/%E4%BD%BF%E7%94%A8ConfigFilter)                                                               | public void com.alibaba.druid.pool.DruidAbstractDataSource.setPassword(java.lang.String)                                      |
| passwordCallback                          | null            | 可以自定义实现定制的PasswordCallback，然后实现定制的密码解密效果                                                                                                                                                                         | public void com.alibaba.druid.pool.DruidAbstractDataSource.setPasswordCallback(javax.security.auth.callback.PasswordCallback) |
| phyTimeoutMillis                          | -1              | 强制回收物理连接的最大超时时长，大于0的情况下才生效，当物理创建之后存活的时长超过该值时，该连接会强制销毁，便于重新创建新连接，建议可以配置成7小时的毫秒值，比如25200000，这样可以规避MySQL的8小时连接断开问题                                                                                                  | public void com.alibaba.druid.pool.DruidAbstractDataSource.setPhyTimeoutMillis(long)                                          |
| poolPreparedStatements                    | false           | 是否缓存preparedStatement，也就是PSCache。PSCache对支持游标的数据库性能提升巨大，比如说oracle。在mysql下建议关闭。                                                                                                                                   | public void com.alibaba.druid.pool.DruidDataSource.setPoolPreparedStatements(boolean)                                         |
| proxyFilters                              |                 | 类型是List<com.alibaba.druid.filter.Filter>，如果同时配置了filters和proxyFilters，是组合关系，并非替换关系                                                                                                                                | com.alibaba.druid.pool.DruidAbstractDataSource.setProxyFilters(List)                                                          |
| queryTimeout                              | 0               | 控制查询结果的最大超时，单位是秒，大于0才生效，最终底层调用是java.sql.Statement.setQueryTimeout(int)                                                                                                                                           | public void com.alibaba.druid.pool.DruidAbstractDataSource.setQueryTimeout(int)                                               |
| removeAbandoned                           | false           | 是否回收泄露的连接,默认不开启，建议只在测试环境设置未开启，利用测试环境发现业务代码中未正常关闭连接的情况                                                                                                                                                            | public void com.alibaba.druid.pool.DruidAbstractDataSource.setRemoveAbandoned(boolean)                                        |
| removeAbandonedTimeoutMillis              | 300000          | 开启回收泄露连接的最大超时，默认300秒表示连接被借出超过5分钟后，且removeAbandoned开启的情况下，强制关闭该泄露连接                                                                                                                                               | public void com.alibaba.druid.pool.DruidAbstractDataSource.setRemoveAbandonedTimeoutMillis(long)                              |
| socketTimeout                             | 0               | 新增的控制创建连接时的socket最大读超时，单位是毫秒，默认0表示永远等待，配置成10000则表示db操作如果在10秒内未返回应答，将抛出异常，工作原理是在创建连接时将该值设置到对应数据库驱动的属性信息中由其JDBC驱动进行控制                                                                                              | public void com.alibaba.druid.pool.DruidAbstractDataSource.setSocketTimeout(int)                                              |
| testOnBorrow                              | false           | 申请连接时执行validationQuery检测连接是否有效，做了这个配置会降低性能，其实一般情况下都可以开启，只有性能要求极其高且连接使用很频繁的情况下才有必要禁用。                                                                                                                             | public void com.alibaba.druid.pool.DruidAbstractDataSource.setTestOnBorrow(boolean)                                           |
| testOnReturn                              | false           | 归还连接时执行validationQuery检测连接是否有效，做了这个配置会降低性能，这个一般不需要开启。                                                                                                                                                            | public void com.alibaba.druid.pool.DruidAbstractDataSource.setTestOnReturn(boolean)                                           |
| testWhileIdle                             | true            | 建议配置为true，不影响性能，并且保证安全性。申请连接的时候检测，如果空闲时间大于timeBetweenEvictionRunsMillis，执行validationQuery检测连接是否有效。                                                                                                               | public void com.alibaba.druid.pool.DruidAbstractDataSource.setTestWhileIdle(boolean)                                          |
| timeBetweenEvictionRunsMillis             | 60000           | 有两个含义：  <br>1) Destroy线程会检测连接的间隔时间，如果连接空闲时间大于等于minEvictableIdleTimeMillis则关闭物理连接。  <br>2) testWhileIdle的判断依据，详细看testWhileIdle属性的说明                                                                               | public void com.alibaba.druid.pool.DruidAbstractDataSource.setTimeBetweenEvictionRunsMillis(long)                             |
| transactionQueryTimeout                   | 0               | 控制查询结果的最大超时，单位是秒，大于0才生效，最终是在开启事务的情况下底层调用java.sql.Statement.setQueryTimeout(int)                                                                                                                                  | public void com.alibaba.druid.pool.DruidAbstractDataSource.setTransactionQueryTimeout(int)                                    |
| url                                       |                 | 连接数据库的url，不同数据库不一样。例如：  <br>mysql : jdbc:mysql://10.20.153.104:3306/druid2  <br>oracle : jdbc:oracle:thin:@10.20.149.85:1521:ocnauto                                                                             | com.alibaba.druid.pool.DruidAbstractDataSource.setUrl(String)                                                                 |
| username                                  | null            | 连接数据库的用户名                                                                                                                                                                                                        | public void com.alibaba.druid.pool.DruidAbstractDataSource.setUsername(java.lang.String)                                      |
| validationQuery                           | null            | 用来检测连接是否有效的sql，要求是一个查询语句，常用select 'x'。如果validationQuery为null，testOnBorrow、testOnReturn、testWhileIdle都不会起作用。                                                                                                      | public void com.alibaba.druid.pool.DruidAbstractDataSource.setValidationQuery(java.lang.String)                               |
| validationQueryTimeout                    | -1              | 单位：秒，检测连接是否有效的超时时间，大于0才生效。底层调用jdbc Statement对象的void setQueryTimeout(int seconds)方法                                                                                                                               | public void com.alibaba.druid.pool.DruidAbstractDataSource.setValidationQueryTimeout(int)                                     |


## 一、基础连接配置(9项)

| 配置项                           | 类型         | 默认值        | 选择   | 说明                                                    |
| ----------------------------- | ---------- | ---------- | ---- | ----------------------------------------------------- |
| `url`                         | String     | null       | ✅保持  | JDBC 连接 URL                                           |
| `username`                    | String     | null       | ✅保持  | 数据库用户名                                                |
| `password`                    | String     | null       | ✅保持  | 数据库密码                                                 |
| `driverClassName`             | String     | null（自动检测） | 🔒默认 | JDBC 驱动类名                                             |
| `connectProperties`           | Properties | 空          | 🔒默认 | 传递给 JDBC 驱动的额外属性                                      |
| `defaultAutoCommit`           | boolean    | true       | 🔒默认 | 连接默认自动提交状态                                            |
| `defaultReadOnly`             | Boolean    | null       | 🔒默认 | 连接默认只读状态                                              |
| `defaultTransactionIsolation` | Integer    | null       | 🔒默认 | 默认事务隔离级别                                              |
| `defaultCatalog`              | String     | null       | 🔒默认 | 默认 catalog （catalog 就是 schema/database，SQL 不写库名时的默认值） |
|                               |            |            |      |                                                       |

---

## 二、连接池大小配置（6 项）

| 配置项                        | 类型   | 默认值    | 选择      | 说明                 |
| -------------------------- | ---- | ------ | ------- | ------------------ |
| `initialSize`              | int  | 0      | 🔄需要考虑  | 启动时初始化的连接数         |
| `maxActive`                | int  | 8      | 🔄动态决定  | 最大活跃连接数            |
| `minIdle`                  | int  | 0      | 🔄确定默认值 | 最小空闲连接数            |
| `maxIdle`                  | int  | 8      | ✅保持     | 【完全废弃】getter 无任何引用 |
| `maxWait`                  | long | -1（不限） | ✅保持2000 | 获取连接的最大等待时间（毫秒）    |
| `notFullTimeoutRetryCount` | int  | 0      | 🔒默认    | 连接池满时的重试次数         |
|                            |      |        |         |                    |
|                            |      |        |         |                    |
- maxIdle 完全无任何引用，纯粹是 dbcp 拿过来的无用选项
- notFullTimeoutRetryCount：这是一个在**连接池没满**的情况下，拿连接失败后自动重试的机制
- [问题 1] druid 创建连接是一个 try 方法，封装了哪些细节，失败的时候会做什么。
	- 主要方法：`DruidDataSource#getConnection(long maxWaitMillis)`
	- 核心逻辑：`DruidDataSource#getConnectionDirect(long maxWaitMillis)`
	- 核心逻辑`DruidDataSource#getConnectionInternal(long maxWait)`
	- 
	- `maxWait`：最大等待时间 
	- [TODO]`maxWaitThreadCount`: 这个还不清楚
	- 以下文段采用深度优先搜索，每次我们先说完一个点的后续，但整体是顺序的
	- 拿连接时，判断 活跃计数 和 空闲计数（poolingCount）是否小于 `maxActive`
		- 拿到连接后`poolingCount--; activeCount++;`（注意纯新建时，直接变活跃，无poolingCount变化）
	- 拿不到连接时，会阻塞，阻塞队列相关的设计中，有两个主要概念
		- 1. 阻塞队列，代表着排着队等待拿连接的具体线程
			- 线程拿不到连接会释放cpu，等待唤醒
		- 2. 等待线程计数：这是一个 int 统计量，用来限制可以排队的线程数量
			- 是否有可配置的地方呢？
	- 建连接、给阻塞线程发连接的过程，是一个条件状态的交互过程
		- 主要思路是：拿取一个有需求的线程，在可以满足需求时通知它
		- 可以只关注带有超时时间的**需求满足**过程`pollLast(long startTime, long expiredTime)`
	- 满足需求的流程
		- 1. 如果poolCount=0，则发送`empty.signal()`，唤醒正在等待这个条件的人。同时启动**一个建连任务**，
		- 2. `notEmpty.await(long time, 毫秒/秒等单位)`睡眠等待建连成功（`notEmpty`信号），睡眠时间是`超时时间-启动时间`
		- 建连和等待连接，通过`emptyWaitThreadCount`和`notEmptyWaitThreadCount`来进行统计。统计等待各类信号的数量。
	- 读到这里，`maxWaitThreadCount` 的作用似乎明朗了，可以用来控制，这样一批通过信号等待的线程队列的大小。
	- 而`notFullTimeoutRetryCount`的作用也明朗了，它直接尝试在**超时**错误时，如果连接池未满，则进行重试，这里包含了所有
- 以上过程过完后，连接基本取到了
	- 开始进行连接验证
	 
---

## 三、连接验证配置（7 项）

| 配置项                      | 类型                     | 默认值           |                                | 说明                    |
| ------------------------ | ---------------------- | ------------- | ------------------------------ | --------------------- |
| `validationQuery`        | String                 | null          | ✅保持                            | 用于验证连接有效性的 SQL，不写有默认值 |
| `validationQueryTimeout` | int                    | -1            | 🔄可以设一个值，虽然不设会被socketTimeout兜底 | 验证查询超时时间（秒）           |
| `testOnBorrow`           | boolean                | false         | 🔄同步位点探活，是否开启                  | 借出连接时是否验证             |
| `testOnReturn`           | boolean                | false         | 🔄同步位点探活，是否开启                  | 归还连接时是否验证             |
| `testWhileIdle`          | boolean                | true          | 🔄异步定时探活任务                     | 空闲时是否验证连接             |
| `validConnectionChecker` | ValidConnectionChecker | null（DB 自动适配） | 🔒默认                           | 自定义连接验证实现             |
| `useUnfairLock`          | boolean                | true          | 🔒默认                           | 是否使用非公平锁获取连接【默认非公平】   |
|                          |                        |               |                                |                       |
- 关键[useUnfairLock] 1.2.22 之后删除了和 maxWait 的联动。 1.2.22  之前，maxWait 启用时，会默认采取**公平锁**，而公平锁会降低并发效率。
	- 【1.2.22 之前】需要配置 maxWait 和 useUnfairLock=true
	- 【1.2.22 之后】只需配置 maxWait, useUnfaiLock 默认为true。
- 连接验证的优先级是：testOnBorrow
	- 开启了后，每次获取连接后，都会执行一次连接校验，若未通过则进入下一个死循环，尝试获取连接
	- 若未开启，则尝试查看连接是否已关闭。否则进入下一个死循环，尝试获取连接
		- 空闲校验
			- 读取上一次`lastActiveTimeMillis`，查看现在时间戳到上次活跃是否**超过**了 `timeBetweenEvictionRunsMillis`
		- 删除废弃`removeAbandoned`：
			- 这个标志开了以后，会维护一个`activeConnections`的map中。
			- 后续和取连接过程解耦，另一个线程去消费活跃线程，进行废弃检测。
		- 在最后根据`defaultAutoCommit 为 false`，强行设置一下false。
- `TestConnectionInternal`方法是探活的核心代码
	- 入参`DruidConnectionHolder holder`携带很多**最后一次xx的时间**
	- 探活核心的两个配置是`validationQuery`，和`validationQueryTimeout`，第一个是一个SQL，通常默认`SELECT 1;`，会真的连库执行该SQL，第二个
		- 注意`validationQuery`通常会失效，需要配置String property = properties.getProperty("druid.mysql.usePingMethod");
		- validationQueryTimeout 默认值是-1，会无限等待
- `close()`方法-`recycle(DruidPooledConnection conn)`方法：归还连接时`testOnReturn`
	- 从`activeConnections`里移除该连接
	- [TODO]处理连接与线程关系
	- 回收过程中对链接执行探活
	- **计算当前时间到连接创建时间** `holder.connectTimeMillis`之间的时间差，与配置项**保活时间**`phyTimeoutMillis`进行比对。如果超时则销毁连接
	- `putLast(holder, lastActiveTimeMillis)`来把连接放回去
	- 释放一个`notEmpty.signal()`，尝试唤醒阻塞在`notEmpty`上的线程
---

## 四、PreparedStatement 缓存配置（4 项）

| 配置项                                         | 类型      | 默认值   | 选择              | 说明                             |
| ------------------------------------------- | ------- | ----- | --------------- | ------------------------------ |
| `poolPreparedStatements`                    | boolean | false | ✅保持             | 是否开启 PreparedStatement 缓存      |
| `sharePreparedStatements`                   | boolean | false | 🔒默认【会有全局同步锁代价】 | 是否在连接间共享 PreparedStatement     |
| `maxPoolPreparedStatementPerConnectionSize` | int     | 10    | ✅保持50           | 每个连接最多缓存的 PreparedStatement 数量 |
| `maxOpenPreparedStatements`                 | int     | -1    |                 | 同上（别名）                         |
- 这里对`PreparedStatement`做的**池化**到底解决什么问题？
	- `PreparedStatement`本身就有缓存的设计意图，一个statement预编译后只需替换参数，少走很多流程
		- 但其问题在于，它不能**跨调用复用**，通常只是一个业务方法里的多个参数之间生效。
		- 将其池化，可以在多次调用之间复用，减少编译成本。
	- 需要区分：`preparedStatement`的缓存是**发生在client侧**还是**server侧**。
		- `JDBC connector`实现中，默认是关闭服务侧缓存的（`useServerPrepStmts`=false)
		- 也就是说，不考虑池化时，preparedStatement 本身的作用，主要是JVM逻辑成本，这包括拼SQL，替换参数，设置执行前的一些上下文信息等。
		- 池化后则是进一步跨调用优化这层成本。
- Druid 里 `sharePreparedStatements`是否值得额外考虑
	- 是，因为 sharePreparedStatements 在连接层级之上进一步提供了 `PreparedStatement`的缓存，进一步提升了 client 侧缓存的效果。
---

## 五、连接驱逐与保活配置（8 项）

| 配置项                             | 类型      | 默认值           |             | 说明                                   |
| ------------------------------- | ------- | ------------- | ----------- | ------------------------------------ |
| `timeBetweenEvictionRunsMillis` | long    | 60000（1分钟）    | ✅保持60秒      | 驱逐线程运行间隔（毫秒）                         |
| `numTestsPerEvictionRun`        | int     | 3             | 🔄需要根据连接数计算 | 每次驱逐检测的连接数                           |
| `minEvictableIdleTimeMillis`    | long    | 1800000（30分钟） | ✅保持 5分钟     | 连接最小空闲时间，超过才可被驱逐（毫秒）                 |
| `maxEvictableIdleTimeMillis`    | long    | 25200000（7小时） | 🔄是否保持      | 【强制驱逐，不考虑minIdle】连接最大空闲时间，超过强制驱逐（毫秒） |
| `keepAlive`                     | boolean | false         | ✅保持开启       | 是否开启连接保活                             |
| `keepAliveBetweenTimeMillis`    | long    | 120000（2分钟）   | ✅保持2分钟      | 保活检测间隔（毫秒）                           |
| `phyTimeoutMillis`              | long    | -1（不限）        | 🔄可考虑设置该项   | 物理连接的最大存活时间（毫秒）                      |
| `phyMaxUseCount`                | long    | -1（不限）        | 🔒默认【不限次数】  | 物理连接最大使用次数                           |
|                                 |         |               |             |                                      |
- DestroyTask定时维护空闲线程状态，包括【**一个任务**同时连接**驱逐和保活两部分**】，这是【一个定时任务】
	- 保活配置（`keepAlive`）需要额外开启，开启后才会探活+重建连接
- 决策流程：
- ```
  1. 物理连接是否太老？
   phyTimeoutMillis 命中 => close

2. 物理连接使用次数是否太多？
   phyMaxUseCount 命中 => close

3. idle 是否超过 maxEvictableIdleTimeMillis？
   命中 => 强制 close

4. idle 是否超过 minEvictableIdleTimeMillis？
   如果 idle 数量超过 minIdle => close
   如果需要保留 minIdle 且 keepAlive=true => 探活保活

5. idle 是否超过 keepAliveBetweenTimeMillis？
   keepAlive=true 时，可能执行保活探测

6. 都不满足
   保留
  ```
---

## 六、超时配置（5 项）

| 配置项                       | 类型  | 默认值                | 选择                       | 说明                                     |
| ------------------------- | --- | ------------------ | ------------------------ | -------------------------------------- |
| `connectTimeout`          | int | 0（驱动默认）【mysql 是无限】 | 🔄可考虑设位置                 | 【**主要是TCP三次握手**、MySQL握手等】建立连接的超时时间（毫秒） |
| `socketTimeout`           | int | 0（驱动默认）【mysql 是无限】 | 🔄考虑properties和Setter的权衡 | Socket 读写超时时间（毫秒）                      |
| `queryTimeout`            | int | 0（不限）【mysql 是无限】   | 🔒默认                     | 【SQL执行时间】默认查询超时时间（秒）                   |
| `transactionQueryTimeout` | int | 0（同 queryTimeout）  | 🔒默认                     | 事务中的查询超时时间（秒）                          |
| `maxWaitThreadCount`      | int | -1（不限）             | 🔒默认                     | 最大等待获取连接的线程数                           |


## 关于networkTimeout 与 socketTimeout
socketTimeout是socket读操作的等待时间限制，通常指“等待mysql返回包”
```
发送 SQL  
↓  
阻塞在 socket.read() 等服务端返回第一个包
```

JDBC MySQL connector 源码：https://raw.githubusercontent.com/mysql/mysql-connector-j/release/9.x/src/main/user-impl/java/com/mysql/cj/jdbc/ConnectionImpl.java
注意 **jdbc 层的 `setNetworkTimeout` 就是 mysql 底层的`setSocketTimeout`**
```
    @Override
    public void setNetworkTimeout(Executor executor /* not used */, int milliseconds) throws SQLException {
        SecurityManager sec = System.getSecurityManager();
        if (sec != null) {
            sec.checkPermission(SET_NETWORK_TIMEOUT_PERM);
        }

        if (milliseconds < 0) {
            throw SQLError.createSQLException(Messages.getString("Connection.27"), MysqlErrorNumbers.SQLSTATE_CONNJ_ILLEGAL_ARGUMENT,
                    getExceptionInterceptor());
        }

        Lock connectionLock = getConnectionLock();
        connectionLock.lock();
        try {
            checkClosed();
            getSession().setSocketTimeout(milliseconds);
        } finally {
            connectionLock.unlock();
        }
    }
```
---

## 七、废弃连接处理配置（3 项）

| 配置项                            | 类型      | 默认值         | 说明                |
| ------------------------------ | ------- | ----------- | ----------------- |
| `removeAbandoned`              | boolean | false       | 是否自动回收废弃连接        |
| `removeAbandonedTimeoutMillis` | long    | 300000（5分钟） | 连接被认定为废弃的超时时间（毫秒） |
| `logAbandoned`                 | boolean | false       | 是否记录废弃连接的堆栈信息     |
|                                |         |             |                   |
|                                |         |             |                   |
- 定义：什么是**废弃连接**
	- “借走连接但迟迟不归还”，连接池帮你**强制回收（close）**。
	- 主要考虑连接的上次使用时间：`当前时间 - lastActiveTime > timeout`
- 调用时机：
	- `eviction定时任务`
	- `borrow`时同步触发
![[Pasted image 20260423155411.png|278]]
---

## 八、初始化与行为配置（5 项）

| 配置项                         | 类型           | 默认值   | 选择                | 说明                        |
| --------------------------- | ------------ | ----- | ----------------- | ------------------------- |
| `asyncInit`                 | boolean      | false | 🔄考虑是否开启（等价于预热）   | 是否异步初始化连接                 |
| `failFast`                  | boolean      | false | 🔄影响borrow链路是否做重试 | 连接失败时是否立即抛出异常（不等待）        |
| `connectionInitSqls`        | List<String> | null  |                   | 连接创建后执行的初始化 SQL 列表        |
| `filters`                   | String       | ""（空） |                   | 过滤器列表（逗号分隔，如 `stat,wall`） |
| `killWhenSocketReadTimeout` | boolean      | false |                   | Socket 读超时时是否强制关闭连接       |

---

## 九、监控统计配置（仅连接池行为相关）（4 项）

> 以下属于连接池运行行为，不是外围监控 Servlet/JMX 配置：

| 配置项                         | 类型      | 默认值   | 说明                      |
| --------------------------- | ------- | ----- | ----------------------- |
| `timeBetweenLogStatsMillis` | long    | 0（禁用） | 定期打印统计日志的间隔（毫秒），0 表示不打印 |
| `useGlobalDataSourceStat`   | boolean | false | 是否使用全局统计数据              |
| `resetStatEnable`           | boolean | true  | 是否允许重置统计数据              |
| `logDifferentThread`        | boolean | true  | 是否记录不同线程的操作             |
Druid 的性能监控日志，是后台线程打印的，默认行为是什么日志都不打印。有一个开关，能控制一个进程下的多个 druid 实例的日志是不是打在一起；一个开关控制，是否允许通过 MBean 直接重置统计值；一个控制“跨线程归还”的warn，用来提醒“连接泄露”。