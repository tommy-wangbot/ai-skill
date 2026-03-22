# Template Library

## 1. Universal Robust Template

Use for most prompt optimization tasks.

```text
[Task Objective]
You will complete the following task: <one-sentence goal>.

[Inputs]
Sources:
1) <source A>
2) <source B>

[Execution Phases]
Phase A - <name>:
- Do: <allowed operations>
- Do not: <forbidden operations>

Phase B - <name>:
- Only modify: <scoped content>
- Must preserve: <non-editable content>

[Output Contract]
Return exactly in this structure:
1) <section/table 1>
2) <section/table 2>
Format: <Markdown/JSON/CSV>
Do not output process notes.

[Quality Gates]
- Completeness: no missing required items.
- Consistency: terminology and mapping are aligned.
- Boundary: no forbidden rewrite in protected phase.
```

Default delivery mode for this skill:
- Provide `长版中文优化稿` first
- Provide `短版中文优化稿` second
- Keep both directly usable (paste-ready)

## 2. Extraction Then Adjustment (High-Risk Mixed Task)

Use when source fidelity and later adjustment must both happen.

```text
任务说明
请基于以下资料完成两阶段任务：
1) <文件1>
2) <文件2>
3) <策略/变更文件>

第一阶段：原文结构化整理（不得改写）
- 按固定表头输出：<表头顺序>
- 仅做原文摘取，不合并、不总结、不改写
- 对编号条目（如 (1)(2)）按行拆分展示

第二阶段：定向调整（允许改写）
- 仅针对 <指定范围> 调整职责归属与措辞
- 其余内容保持与第一阶段一致
- 调整后需符合 <策略文件> 口径

输出要求
- 先输出【第一阶段结果】
- 再输出【第二阶段结果】
- 使用 <Markdown 表格/JSON>，不输出解释性文字

质量校验
- 第一阶段字段覆盖完整
- 第二阶段仅在允许范围内改动
- 两阶段数据行数与主键映射可核对
```

## 3. Short Prompt Compression (2-3 Sentences)

Use when user asks for concise prompts.

```text
请将以下内容处理为<目标语言/格式>，保持<语气/文体>。
优先保留原文的逻辑结构、关键约束与概念密度，避免无依据扩写或过度意译。
若存在分析性或系统性内容，按<研究型/技术文档>表达输出。
```

## 3.1 Dual-Version Chinese Output Wrapper (Default)

```text
请输出两版中文优化提示词：
【长版中文优化稿】完整保留目标、约束、边界、输出格式与校验规则；
【短版中文优化稿】压缩表达但不得丢失硬约束（输入范围、禁止项、输出结构）。
除这两版外不输出冗余说明。
```

## 4. Anti-Omission Add-on

Append when outputs often drop rows/fields.

```text
防漏要求：
- 对每个来源逐项扫描并映射到输出字段，不得跳项。
- 输出后执行一次覆盖核对：逐项列出已覆盖条目数与未覆盖条目（如有）。
- 若发现冲突或缺失，先标注再继续，不得静默省略。
```

## 5. Model Tuning Notes (DeepSeek/Qwen)

- Specify role and boundaries early; these models react strongly to task framing.
- Use explicit "do not rewrite" or "only modify X" constraints.
- Keep long prompts segmented with clear headings and ordered rules.
- Require deterministic output structure to reduce style drift.
