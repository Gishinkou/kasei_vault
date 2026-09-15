# 字母频率覆盖
如果只看字母频率，我建议用“单词覆盖率”：

> 某字母出现在 2,315 个候选答案中的多少个单词里。


评分规则：

\[ Score=\sum_{\text{不重复字母}} P(\text{答案包含该字母}) \]

例如：

```
STERN = S + T + E + R + N
      = 26.7% + 28.8% + 45.6% + 36.2% + 23.8%
      = 161.0%
```

这里 161% 不是概率，而是表示：随机答案平均包含 `S/T/E/R/N` 中的 **1.61 个字母**。

### 单词排名

|排名|单词|纯频率分|
|---|---|---|
|1|`STERN`|**1.610**|
|2|`MANOR`|1.411|
|3|`BLAST`|1.343|
|4|`CLOTS`|1.319|
|5|`RIGHT`|1.223|
|6|`SLING`|1.194|
|7|`CRYPT`|1.173|
|8|`CHORD`|1.169|
|9|`LIGHT`|1.141|
|10|`DRINK`|1.126|
# 字母频率两两组合
### 两行组合排名

两行之间重复的字母只计一次：

|排名|两行组合|覆盖字母|纯频率分|
|---|---|---|---|
|1|`STERN + CLUMP`|C E L M N P R S T U|**2.559**|
|2|`MANOR + LIGHT`|A G H I L M N O R T|2.552|
|3|`STERN + GLYPH`|E G H L N P R S T Y|2.513|
|4|`BLAST + CHORD`|A B C D H L O R S T|2.512|
|5|`STERN + PLUMB`|B E L M N P R S T U|2.481|
|6|`BLAST + DRINK`|A B D I K L N R S T|2.469|
|7|`STERN + LIGHT`|E G H I L N R S T|2.463|
|8|`CLOTS + DRINK`|C D I K L N O R S T|2.445|
|9|`CLOTS + BRING`|B C G I L N O R S T|2.443|
|10|`MANOR + CLOTS`|A C L M N O R S T|2.440|

所以：

- **只看字母频率：`STERN → CLUMP` 第一**
- **看真实颜色反馈熵：`BLAST → CHORD` 第一**
- `MANOR → LIGHT` 在两套算法中都很强

区别在于纯频率认为“覆盖高频字母越多越好”，但不关心字母位置、字母之间的相关性，也不关心最终颜色能否区分候选。

如果你的策略是固定用前两行扫字母，我会倾向 `STERN + CLUMP`；如果目标是数学上最大化实际排除量，则选 `BLAST + CHORD`。数据基于[原始 2,315 个 Wordle 答案](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b)。


对，这属于“固定两行、非自适应开局”。必须计算两次颜色反馈的联合熵，不能把两个单词的单词熵直接相加。

基于原始 2,315 个答案，两词顺序不影响联合熵；表中把单词熵较高的放第一行：

|排名|两行组合|不重复字母|联合熵|平均剩余|最坏剩余|
|---|---|---|---|---|---|
|1|`BLAST + CHORD`|10|**8.800 bit**|**9.90**|50|
|2|`STERN + CLUMP`|10|8.696|11.26|69|
|3|`MANOR + LIGHT`|10|8.691|9.95|**42**|
|4|`BLAST + DRINK`|10|8.690|10.45|63|
|5|`CLOTS + DRINK`|10|8.623|11.25|60|
|6|`CLOTS + BRING`|10|8.622|11.02|58|
|7|`SLING + CRYPT`|10|8.566|11.18|66|
|8|`MANOR + CLOTS`|9|8.536|11.07|50|
|9|`SLING + CHORD`|10|8.504|12.02|58|
|10|`STERN + PLUMB`|10|8.487|12.90|71|

指标含义：

- 联合熵：越高，平均信息量越大。
- 平均剩余：随机答案在获得两行反馈后，平均还剩多少候选。
- 最坏剩余：运气最差的颜色反馈下，最多还会剩多少候选。

结论很清晰：

1. **追求平均信息量：`BLAST → CHORD`**
    
    覆盖 `B L A S T C H O R D`，没有重复字母。两行后平均从 2,315 个压缩到约 **9.9 个**。
    
2. **追求最坏情况稳定：`MANOR → LIGHT`**
    
    平均剩余约 9.95，略逊于第一名，但最坏只剩 **42 个**，是这些组合里最稳的。
    
3. **偏爱高频辅音：`STERN → CLUMP`**
    
    覆盖 `S T E R N C L U M P`，结构很好，不过平均剩余 11.26，不如前两组。
    

一个重要现象：`STERN` 是这些词里最强的单行盲猜，但最强两行组合却是 `BLAST + CHORD`。原因是组合价值取决于两个词的**互补性和联合反馈分布**，不是第一行分数最高就一定赢。

虽然零字母重复通常更好，但也不是绝对规则。例如 `MANOR + CLOTS` 重复 `O`，仍排第 8，因为高频字母和位置分布很有价值。

如果你固定占用前两行，我建议：

- 平均最优：`BLAST → CHORD`
- 风险最小：`MANOR → LIGHT`
- 辅音扫描：`STERN → CLUMP`

这是按照[原始 Wordle 2,315 答案词表](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b)计算；最大化反馈联合熵的依据可参见[信息论 Wordle 方法](https://labs.acme.byu.edu/Volume3/InformationTheory/InformationTheory.html)。固定两行会放弃根据第一行颜色调整第二行的机会，而且在 Hard Mode 下第二行未必合法。


你说得对，Wordle 中后期的难点往往是区分辅音。`L/M/N/R` 很难由一个常见五字母词全部覆盖，但其实不必全测。

比如候选是：

`LIGHT / MIGHT / NIGHT / RIGHT`

猜 `MANOR` 就能同时测试 `M/N/R`：

- M 命中 → `MIGHT`
- N 命中 → `NIGHT`
- R 命中 → `RIGHT`
- 三者全灰 → `LIGHT`

适合高覆盖测试辅音的词：

|单词|主要测试的辅音|
|---|---|
|`CRYPT`|C、R、P、T|
|`NYMPH`|N、M、P、H|
|`GLYPH`|G、L、P、H|
|`CLUMP`|C、L、M、P|
|`WRUNG`|W、R、N、G|
|`BRICK`|B、R、C、K|
|`DRINK`|D、R、N、K|
|`FLING`|F、L、N、G|
|`CHORD`|C、H、R、D|
|`PLUMB`|P、L、M、B|
|`STERN`|S、T、R、N|
|`BLAST`|B、L、S、T|

两词组合覆盖更多辅音：

- `CLUMP + BRING`：C、L、M、P、B、R、N、G
- `NYMPH + CLOTS`：N、M、P、H、C、L、T、S
- `CRYPT + SLING`：C、R、P、T、S、L、N、G
- `BRICK + GLYPH`：B、R、C、K、G、L、P、H

我的推荐是记住这几个“工具词”：

- 测常见辅音：`STERN`
- 测 L/M/P/C：`CLUMP`
- 测 N/M/P/H：`NYMPH`
- 极限辅音覆盖：`CRYPT`
- 综合补漏：`BRING`

关键不是覆盖的辅音越多越好，而是覆盖**当前候选之间不同的那些字母**。像 `MANOR` 那样一次区分四个答案，价值通常比盲猜 `CRYPT` 更高。


有。用 Shannon 信息熵衡量：把每个猜词产生的绿/黄/灰反馈分组，分得越均匀，熵越高，盲猜价值越大。最大理论反馈虽有 \(3^5=243\) 种，但实际远少于此；最大化反馈熵等价于尽量降低答案的不确定性。[信息论原理说明](https://labs.acme.byu.edu/Volume3/InformationTheory/InformationTheory.html)

我用原始 2,315 个 Wordle 答案、每个答案等概率计算，词表来自[原始 Wordle 答案列表](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b)。

|排名|猜词|信息熵|猜后平均剩余候选|
|---|---|---|---|
|1|`STERN`|**5.358 bit**|**98.0**|
|2|`BLAST`|5.120|140.7|
|3|`MANOR`|5.113|122.6|
|4|`CLOTS`|5.006|135.0|
|5|`SLING`|4.743|177.3|
|6|`CHORD`|4.676|208.3|
|7|`CRYPT`|4.623|177.3|
|8|`RIGHT`|4.614|184.2|
|9|`DRINK`|4.515|225.2|
|10|`LIGHT`|4.476|204.1|
|11|`BRING`|4.450|226.1|
|12|`NIGHT`|4.333|241.8|
|13|`BRICK`|4.269|258.0|
|14|`FLING`|4.192|295.4|
|15|`MIGHT`|4.161|279.5|
|16|`CLUMP`|4.149|307.9|
|17|`WRUNG`|4.114|281.4|
|18|`GLYPH`|3.928|320.1|
|19|`PLUMB`|3.853|363.6|
|20|`NYMPH`|3.656|371.3|

结论：

- 这些词里盲猜首选是 **`STERN`**，明显领先。
- 第二梯队是 `BLAST`、`MANOR`、`CLOTS`。
- `CRYPT` 看似覆盖四个辅音，但 `Y/P/C` 的整体频率不够高，所以只排第 7。
- `NYMPH`、`GLYPH` 虽然辅音密集，却包含较低频字母，盲猜价值反而较低。
- `MANOR` 特别适合区分 `LIGHT/MIGHT/NIGHT/RIGHT`，但这是“针对候选集”的价值，不是普遍首猜价值。

如果只记一个辅音型开局词：**`STERN`**。如果已经知道元音，希望集中扫辅音，再根据剩余候选选择 `CRYPT`、`CLUMP` 等工具词。