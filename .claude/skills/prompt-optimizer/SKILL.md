---
name: prompt-optimizer
description: High-quality prompt optimization for turning vague or unstable prompts into reliable, testable instructions with explicit goals, scope, constraints, rewrite boundaries, and output formats. Use when asked to optimize/refine/rewrite prompts, improve output stability, reduce ambiguity, prevent missing items, enforce extraction-vs-rewrite boundaries, or adapt prompts for models such as DeepSeek, Qwen, ChatGPT, and Claude.
---

# Prompt Optimizer

## Overview

Convert rough prompts into production-ready prompts that are hard to misinterpret.
Prioritize explicit constraints, phase separation, and output contracts over stylistic polishing.
Default to Chinese deliverables with two versions: `长版` and `短版`.

## Activation Priority

This skill is for prompt work first, not task execution.

When this skill is explicitly named by the user, or the user asks to optimize/refine/rewrite a prompt, you must treat the request as a prompt-optimization task unless the user explicitly asks for both optimization and execution.

Default behavior when activated:
- Optimize the prompt.
- Clarify scope, constraints, phases, and output contract.
- Stop at the optimized prompt and notes.

Do not automatically continue into research, coding, analysis, browsing, or final task execution after producing the optimized prompt unless the user explicitly asks for a second step such as "然后执行", "再按这个 prompt 去做", or equivalent.

If the user's message mixes two intents, such as "先优化提示词，再帮我研究", split them into:
1. Current turn or current step: optimize the prompt only.
2. Optional next step: execute the optimized prompt only after explicit confirmation or instruction.

## Non-Goals And Boundaries

When this skill is active, these are forbidden unless explicitly requested:
- Answering the underlying business question directly
- Starting web research for the substantive task
- Producing the final report, code, analysis, recommendations, or solution itself
- Silently treating "optimize" as "optimize and execute"

If examples are needed, provide examples of prompt wording, not the actual solved output.

## Workflow

### 1. Diagnose the Prompt

Identify:
- Target model and use case
- Task type: extraction, transformation, generation, analysis, or mixed
- Main failure mode: ambiguity, missing rows, over-rewrite, format drift, hallucination

If the prompt mixes incompatible goals, split it into phases before rewriting.

### 2. Extract Hard Requirements

Capture and preserve non-negotiables:
- Required sources, fields, entities, and ordering
- Must/must-not rules
- Output format and section order
- Domain tone and terminology

Separate requirements into:
- `Locked constraints`: never changed by the model
- `Editable constraints`: may be rewritten in allowed phases

### 3. Build a Phase Plan

Use explicit staged execution for mixed tasks.

Default pattern for high-risk business prompts:
1. `Phase A (No rewrite)`: extract/structure faithfully
2. `Phase B (Controlled rewrite)`: adjust only scoped content
3. `Phase C (Final output)`: emit in strict format

State rewrite boundary with direct language such as:
- "Phase A: do not summarize, merge, infer, or rewrite."
- "Phase B: only modify X; keep all other content unchanged."

### 4. Compose the Optimized Prompt

Use the template structure below:
1. Task objective
2. Inputs and source list
3. Phase-by-phase instructions
4. Allowed vs forbidden operations
5. Output contract (format, order, naming, no extra prose)
6. Quality checks (completeness and consistency)

Load concrete templates from `references/template-library.md` when needed.

### 5. Add Quality Gates

Add explicit verification checks in the prompt:
- Completeness check: no missing rows/fields/entities
- Boundary check: forbidden edits did not occur
- Format check: exact schema/order respected

For long tables or multi-source extraction, require row-level coverage confirmation.

### 6. Deliver Optimization Result

Return:
- `长版中文优化稿` (fully constrained, robust version)
- `短版中文优化稿` (compressed, 2-5 lines while preserving hard constraints)
- Brief change notes explaining why reliability improves
- If the original user request also contains a substantive task, add one short line at the end:
  `如需，我可以下一步按这个优化稿继续执行原任务。`

Unless user explicitly asks for another language or one single version, always output both Chinese versions.

## Pre-Response Self-Check

Before responding, verify all of the following:
- Did I rewrite or optimize the prompt itself, rather than solve the underlying task?
- Did I preserve the user's domain goal and constraints without expanding scope?
- Did I avoid doing research, analysis, coding, or recommendation work that belongs to the next step?
- Did I return both `长版` and `短版` unless the user asked otherwise?
- If execution was not explicitly requested, did I stop after the optimized prompt and brief notes?

If any answer is "no", revise the response before sending.

## Optimization Rules

- Prefer explicit constraints over implied intent.
- Prefer phase separation over one-shot mixed instructions.
- Prefer operational verbs: extract, map, split, preserve, adjust.
- Avoid vague qualifiers such as "尽量" or "适当" unless quantified.
- Preserve user domain wording unless user asks for reframing.
- Output defaults: Chinese first, long and short versions together.

## Variant Selection

Select one primary pattern, then apply minimal edits:
- Structured extraction: use strict schema + no-rewrite phase
- Content rewriting: define editable scope and non-editable scope
- Mixed tasks: enforce two-pass or three-pass workflow
- Short prompt request: keep constraints, compress prose

Use only the relevant template from `references/template-library.md`; do not combine all templates unless necessary.
