---
name: interview-transcription
description: 访谈音频转写全流程系统：选择 ASR 路线运行转写、LLM 纠错、结构化阅读版生成、词库维护、评分表生成。当用户提到"转写"、"访谈转写"、"ASR"、"音频转文字"、"纠错"、"添加词库"、"结构化阅读"、"评分表"、"formal_transcript"、"corrected_transcript"时使用此 skill。
---

# 访谈转写系统

## 项目位置

```
/Users/tommy/Documents/codex/interview_transcription_eval/
├── configs/domain_lexicons/     # 运营商词库 YAML（可直接编辑）
│   ├── telecom.yaml             # 运营商通用词
│   ├── broadcast.yaml           # 广电/机顶盒词
│   └── gehua.yaml               # 歌华专属词
└── prompts/
    ├── correction_system_prompt.md
    ├── gemini_direct_user_prompt.md
    └── structured_reading_system_prompt.md
```

所有命令在项目目录下运行：
```bash
cd /Users/tommy/Documents/codex/interview_transcription_eval
```

---

## 推荐工作流（完整链路）

```
音频文件
  → Step 1: ASR 转写
  → Step 2: LLM 纠错（自动挂载词库）
  → Step 3: 结构化阅读版（可选，用于分析交付）
```

---

## Step 1：ASR 转写路线选择

### 路线对比

| 路线 | 命令 | 中文质量 | 速度 | 适用场景 |
|------|------|----------|------|----------|
| SenseVoice + pyannote | `run-sensevoice-pyannote` | ⭐⭐⭐ | 快（39s/30min） | **主线，中文专用** |
| Gemini 直转 | `run-gemini-direct` | ⭐⭐（长音频不稳定） | 快 | 短音频或快速预览 |

### SenseVoice 转写（主线）

```bash
uv run interview-transcription-eval run-sensevoice-pyannote \
  --audio "/绝对路径/音频.wav" \
  --output-dir "/绝对路径/输出目录"
```

输出到 `输出目录/sensevoice-pyannote/`：
- `raw_transcript.{md,json}` — ASR 原始稿（含清洗前内容）
- `formal_transcript.{md,json}` — 清洗后正式底稿
- `run_record.json` — 耗时、段数等运行记录

### 环境要求

- SenseVoice 路线需要 `HF_TOKEN` 或 `HUGGINGFACE_HUB_TOKEN`
- Gemini 路线需要 `GOOGLE_API_KEY` 或 `GEMINI_API_KEY`
- 本地路线推荐 Apple Silicon Mac（pyannote 用 MPS，SenseVoice 用 CPU）

---

## Step 2：LLM 纠错（自动挂载词库）

输入：Step 1 产出的 `formal_transcript.json`

```bash
uv run interview-transcription-eval run-correct \
  --input-json "/输出目录/<route-id>/formal_transcript.json" \
  --output-dir "/输出目录" \
  --route-id <route-id>
```

`route-id` 与 Step 1 保持一致（如 `sensevoice-pyannote`）。

纠错自动执行三层：
1. **规则预纠错** — `domain_lexicons/*.yaml` 的 `aliases` 直接替换
2. **LLM 分块纠错** — 系统提示自动注入标准词表和短语提示
3. 输出到同一目录：`corrected_transcript.{md,json}` + `correction_record.json`

---

## Step 3：结构化阅读版（可选）

将纠错后的底稿转为结构化分析稿（含访谈要点、摘要）：

```bash
uv run interview-transcription-eval run-gemini-structured \
  --transcript "/输出目录/<route-id>/corrected_transcript.md" \
  --speaker-hint 访谈者 \
  --speaker-hint 被访谈人姓名 \
  --output-dir "/输出目录"
```

---

## 词库维护（随时更新）

发现新的 ASR 错词时，编辑对应 YAML 文件，下次纠错自动生效：

| 文件 | 适用内容 |
|------|---------|
| `gehua.yaml` | 歌华部门名、人名、内部术语 |
| `broadcast.yaml` | 机顶盒、广电、融媒体相关 |
| `telecom.yaml` | 运营商通用（政企、运维等） |

添加格式：
```yaml
aliases:
  错误写法: 正确写法   # 直接替换，高置信
phrase_hints:
  - 需要上下文判断的标准短语   # 注入 LLM 提示
```

**已知高频错误（gehua.yaml）：**
- 增强组 → 终端组
- 研发中径 → 研发中心
- 品方中心 → 平台中心

---

## 附：评分表生成

用于人工评估转写质量：

```bash
uv run interview-transcription-eval make-scorecard \
  --sample-name "技术部访谈-研发中心负责人邹海川" \
  --output-dir "/输出目录"
```

---

## 已验证样本

```
音频：/Users/tommy/Documents/转写效果综合对比/2026-03-23 10_03_07-技术部访谈-研发中心负责人邹海川.wav
飞书参考：同目录 *-飞书.txt
输出目录：/Users/tommy/Documents/转写效果综合对比/output/
```
