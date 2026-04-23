你可以把 **Java 线程状态**当成是对“线程生命周期”的一个**抽象观察窗口**。官方就定义在：

👉 Thread.State

一共 **6 种状态**，不多，但每个都很有用（尤其你现在在看锁/连接池，这些状态能直接帮你定位问题）。

---

# 一、Java 的全部线程状态（总览）

```text
NEW
RUNNABLE
BLOCKED
WAITING
TIMED_WAITING
TERMINATED
```

---

# 二、逐个解释（带工程语义）

---

## 1️⃣ NEW（新建）

```java
Thread t = new Thread(...);
```

👉 线程对象创建了，但：

```text
还没 start()
```

---

## 2️⃣ RUNNABLE（运行中 / 可运行）

👉 这是最容易误解的一个状态

它包含：

```text
✔ 正在执行（Running）
✔ 等待 CPU（Ready）
```

👉 Java **不区分运行 vs 就绪**

---

### 典型情况

```java
t.start();
```

之后线程就进入：

```text
RUNNABLE
```

---

## 3️⃣ BLOCKED（锁阻塞）

👉 **只用于 synchronized！**

```java
synchronized (lock) {
    ...
}
```

如果锁被占用：

```text
→ 进入 BLOCKED
```

---

### ❗关键点

- 只和 **monitor lock（对象锁）**有关
    
- **不包括 ReentrantLock**
    

---

## 4️⃣ WAITING（无限等待）

👉 线程主动挂起，**等待别人唤醒**

---

### 典型 API：

```java
Object.wait()
Thread.join()
LockSupport.park()
Condition.await()
```

---

👉 特点：

```text
没有时间限制，必须被唤醒
```

---

## 5️⃣ TIMED_WAITING（带超时等待）

👉 和 WAITING 类似，但有**超时机制**

---

### 典型 API：

```java
Thread.sleep(1000)
Object.wait(1000)
Condition.await(1, TimeUnit.SECONDS)
LockSupport.parkNanos()
```

---

👉 特点：

```text
时间到了自动醒
```

---

## 6️⃣ TERMINATED（已结束）

```text
线程执行完 run() 方法
```

或异常退出

---

# 三、重点对比（你最需要掌握的）

---

## 🔥 BLOCKED vs WAITING（高频面试 / 工程问题）

|状态|含义|
|---|---|
|BLOCKED|等锁（synchronized）|
|WAITING|等条件（park / wait）|

---

👉 举例：

### BLOCKED

```java
synchronized(lock) {
    // 其他线程进不来
}
```

---

### WAITING

```java
queue is empty
→ thread park()
→ 等待被唤醒
```

---

👉 本质区别：

```text
BLOCKED：被动卡住（抢锁失败）
WAITING：主动挂起（逻辑等待）
```

---

# 四、和你现在研究的内容对齐（非常关键）

---

## 1️⃣ ReentrantLock 用的是哪种状态？

👉 不会用 BLOCKED！

它底层基于：

👉 AbstractQueuedSynchronizer

---

线程状态是：

```text
WAITING / TIMED_WAITING
```

因为：

```java
LockSupport.park()
```

---

## 2️⃣ 连接池线程等待连接

典型流程：

```text
拿连接失败
→ 加入队列
→ park()
→ WAITING
```

---

## 3️⃣ interrupt / timeout 的作用

```text
WAITING → RUNNABLE
```

触发方式：

- unpark()
    
- interrupt()
    
- timeout
    

---

# 五、状态转换图（简化版）

```text
NEW
 ↓ start()
RUNNABLE
 ↓ 竞争锁失败
BLOCKED
 ↓ 获取锁
RUNNABLE
 ↓ wait / park
WAITING
 ↓ timeout / unpark / interrupt
RUNNABLE
 ↓ 执行完
TERMINATED
```

---

# 六、一个你可以直接用的“工程判断技巧”

当你看到线程 dump（非常实用）：

---

## 如果是：

```text
BLOCKED
```

👉 基本判断：

> 🔥 有 synchronized 锁竞争

---

## 如果是：

```text
WAITING (parking)
```

👉 基本判断：

> 🔥 AQS / Lock / 连接池 / 队列在排队

---

## 如果是：

```text
TIMED_WAITING
```

👉 基本判断：

> 🔥 sleep / 超时等待 / 限流策略

---

# 七、一个总结（帮你形成稳定认知）

```text
Java 线程状态 = 对线程“为什么没在跑”的分类
```

---

你可以这样记：

```text
RUNNABLE      → 能跑
BLOCKED       → 等锁（synchronized）
WAITING       → 等别人唤醒（park）
TIMED_WAITING → 等时间或唤醒
TERMINATED    → 已结束
```

---

# 如果你想再深入（很建议）

可以继续拆：

👉 为什么 Java 要区分：

- BLOCKED（monitor）
    
- WAITING（park）
    

👉 AQS 为什么完全绕开 BLOCKED

👉 thread dump 里：

```text
"parking to wait for"
"waiting on condition"
```

这些字符串分别对应什么

---

如果你愿意，我可以帮你：

👉 **结合 Druid / 连接池，画一个“线程状态 + 连接获取”的完整时序图**

这个会直接把你现在研究的锁、队列、超时、interrupt 全串起来。

很好，这个问题问得非常“对味”：**把操作系统里的“进程状态模型”，投影到 Java API 视角**来理解 `park()`。

我们就完全**不谈 OS 细节**，只用 Java 抽象来构建一个清晰模型。

---

# 一、先给你一个“Java版线程状态模型”

你在操作系统课里学到的：

```text
运行 → 就绪 → 阻塞
```

在 Java 里可以对应为（简化版）：

| OS概念        | Java视角                  |
| ----------- | ----------------------- |
| Running（运行） | RUNNABLE（正在执行）          |
| Ready（就绪）   | RUNNABLE（等待 CPU）        |
| Blocked（阻塞） | WAITING / TIMED_WAITING |

👉 关键点：

> Java 把“运行 + 就绪”合并成一个状态：**RUNNABLE**

---

# 二、`park()` 在这个模型里是什么角色？

核心一句话：

> **`park()` = 主动让线程进入 WAITING 状态（挂起），直到被唤醒**

---

## 对比操作系统模型

```text
[RUNNABLE] --调用 park()--> [WAITING]
[WAITING]  --unpark()-->    [RUNNABLE]
```

👉 非常像：

```text
运行 → 阻塞 → 被唤醒 → 就绪 → 再运行
```

---

# 三、`park()` 和其他阻塞 API 的统一理解

Java 里所有“阻塞”API，本质都可以归一为：

|API|本质|
|---|---|
|`Thread.sleep()`|定时 park|
|`Object.wait()`|条件 park|
|`Condition.await()`|条件 park|
|`lock.lock()`|竞争失败 → park|
|`LockSupport.park()`|原始 park|

👉 其中最底层的就是：

👉 LockSupport

---

# 四、`park()` 的核心语义（非常重要）

你可以把它理解成：

```text
“把当前线程挂起，除非我拿到一个‘许可’”
```

---

## 关键机制：Permit（许可证）

这是理解 `park()` 的关键！

每个线程都有一个隐藏的：

```text
permit（0 或 1）
```

---

### 行为规则：

#### 1）调用 park()

```text
if permit == 1:
    消耗 permit → 直接返回（不阻塞）
else:
    进入 WAITING（挂起）
```

---

#### 2）调用 unpark(thread)

```text
给 thread 的 permit = 1
如果 thread 在 WAITING → 唤醒
```

---

# 五、用一个简单流程串起来

```java
LockSupport.park();   // 线程A
```

线程 A：

```text
RUNNABLE → WAITING
```

---

另一个线程：

```java
LockSupport.unpark(threadA);
```

线程 A：

```text
WAITING → RUNNABLE → 继续执行
```

---

# 六、和操作系统模型的“关键差异”

这是你这个问题最核心的点👇

---

## ❗差异1：Java 是“显式阻塞”

操作系统：

```text
线程被调度器强制切换
```

Java：

```text
线程自己调用 park() 才阻塞
```

👉 **Java 是“自愿让出执行权”**

---

## ❗差异2：Java 有“许可机制”（非常重要）

传统 OS 思维：

```text
阻塞 → 唤醒（必须先阻塞）
```

Java `park/unpark`：

```text
unpark 可以先发生！
```

例如：

```java
LockSupport.unpark(thread);
LockSupport.park(); // 不会阻塞
```

👉 因为 permit 已经是 1

---

👉 这个设计解决了一个经典问题：

> ❌ “先 notify 后 wait 导致永远卡死”

---

# 七、用状态机理解（Java版）

你可以用这个模型来记：

```text
          +------------------+
          |                  |
          |     RUNNABLE     |
          |                  |
          +--------+---------+
                   |
                   | park()
                   ↓
          +------------------+
          |                  |
          |     WAITING      |
          |                  |
          +--------+---------+
                   |
                   | unpark()
                   ↓
          +------------------+
          |                  |
          |    RUNNABLE      |
          |                  |
          +------------------+
```

---

# 八、interrupt 在这个模型里的位置

你前面问过 interrupt，这里可以融合起来看：

---

当线程：

```java
LockSupport.park();
```

如果发生：

```java
thread.interrupt();
```

👉 会：

```text
WAITING → RUNNABLE（被唤醒）
```

但：

❗不会自动抛异常（这是和 sleep/wait 的区别）

需要你自己检查：

```java
Thread.interrupted()
```

---

# 九、为什么 AQS / ReentrantLock 都用 park？

因为它非常适合实现：

👉 **“队列 + 阻塞 + 唤醒”模型**

比如：

- 连接池等待连接
    
- 锁竞争失败排队
    
- 条件变量等待
    

---

### 典型流程（你可以类比连接池）

```text
线程来拿资源
    ↓
没有资源
    ↓
加入队列
    ↓
park()（挂起）
    ↓
资源释放
    ↓
unpark() 唤醒一个线程
```

---

# 十、一个工程级总结（你可以直接带走）

👉 用 Java API 的视角看：

```text
park/unpark = Java 提供的“线程阻塞/唤醒原语”
```

它在 Java 世界里的地位，相当于：

```text
“操作系统里的阻塞/唤醒机制”的用户态抽象
```

---

# 十一、帮你建立最终心智模型

你可以这样统一理解所有并发阻塞：

```text
线程运行中
    ↓
条件不满足
    ↓
park() → WAITING（挂起，不占 CPU）
    ↓
条件满足（signal / unpark / interrupt）
    ↓
恢复 RUNNABLE
    ↓
继续执行
```

---

# 如果你想再往上抽象一层（很适合你现在做的事）

你可以把整个 Java 并发模型理解为三层：

```text
业务层：连接池 / 限流 / 队列
    ↓
同步层：ReentrantLock / Condition / AQS
    ↓
原语层：park / unpark
```

---

如果你愿意，我可以帮你把：

👉 **“Druid 获取连接全过程（含 park / condition / 超时 / interrupt）画成一个完整状态机”**

那个图会直接把你现在在研究的所有点串起来。