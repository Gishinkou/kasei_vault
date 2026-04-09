深入理解上下文窗口

https://code.claude.com/docs/en/context-window

## token 数的估计

100 汉字 = 150 token
100 英文单词 = 150 token

一个 codex 的上下文是 258k tokens，粗略估算即 20 万汉字层级
- 17万 2000 个汉字或英文单词

> 速算法：token 的2/3（0.6 倍）即汉字或单词数


## 初始咒语

约 4600 token，约 3000 字

过往其他会话的记忆 680 token， 约 400字

## 工具的加载

### MCP Tool

120 tokens，约 80 字

### SKILLs

**每个SKILL仅保留一行描述**

可通过 `/skillName` 主动触发 SKILL，类似执行一个脚本

**SKILL**不会被`/compact`模型指令压缩，永远保持一句话描述的状况

SKILL 是懒加载的，当且仅当 SKILL 被调用时，内容才会被加载

## GLOBAL preferences—— ~/.claude/CLAUDE.md

## Project CLAUDE.md

这个文件放在具体的目录下面，通过 git 作用于所有团队成员的开发分支

## 阅读代码

一个 `auth.ts`鉴权文件，占据了2400 tokens，也就是约 1800 单词。

经验值：1 行代码≈ 15 token

2400 tokens 约 180 行。

## 路径项目规范

`.claude/rules/`定义了一系列行为规范，通过对代码文件进行模式匹配来触发。可能主要用于不同编程语言的项目规范。如 init 文件，api 文件等

在文件走到特定路径，如`/src/api`，自动识别到这可能是一个RESTful api 文件夹，需要以写 api 的方式来维持代码规范与一致性。

如果命中了`*.test.ts`的命名规则，也会尝试

## subagent

subagent 其实主要就是开了一个新的“agent”会话。让 subagent 执行一批指令后，只返回结果。避免上下文被无关内容污染。

## 压缩上下文

`/compact`
```
Context is at 22.2K tokens. Run `/compact` to summarize older exchanges and free space for more work.
```

