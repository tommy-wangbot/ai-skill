---
name: asr
description: Transcribe audio files to text locally using the coli CLI — no API key needed. Trigger when the user says "transcribe", "ASR", "转录", "识别音频", "语音转文字", or "把这段音频转成文字", or provides an audio file path (mp3, m4a, wav, mp4, aac, etc.).
---

# ASR — Local Speech Recognition

Transcribes audio files to text using `coli asr` with local models. No API calls, no key required. Supports Chinese, English, Japanese, Korean, Cantonese.

## Prerequisites

```bash
# Required: coli CLI
npm install -g @marswave/coli

# Recommended: ffmpeg for non-WAV formats (mp4, m4a, aac...)
brew install ffmpeg        # macOS
sudo apt install ffmpeg    # Ubuntu/Debian
```

On first use, `coli` auto-downloads the speech model (~60 MB) to `~/.coli/models/`.

## Quick Start

```bash
coli asr <audio-file>
```

Example:
```bash
coli asr meeting.m4a
```

## Models

| Model | Languages | Notes |
|-------|-----------|-------|
| `sensevoice` (default) | Chinese, English, Japanese, Korean, Cantonese | Detects language, emotion, audio events |
| `whisper-tiny.en` | English only | Lightweight, English-only |

Use `sensevoice` for multilingual or unknown content.

## Workflow

1. Verify `coli` is installed; prompt user to install if missing
2. Check ffmpeg availability for non-WAV formats
3. Confirm the audio file path and model with the user
4. Run `coli asr <file>` locally — no network calls
5. Display raw transcript in conversation
6. If AI polishing is enabled (default): post-process for punctuation, readability (no summarization, no meaning change)
7. Ask user whether to save as Markdown: `{audio-filename}-transcript.md`

## Output Format

Saved Markdown includes front-matter metadata:

```markdown
---
source: meeting.m4a
date: 2026-03-24
model: sensevoice
duration: 00:32:14
language: zh
---

# Transcript
...
```

## Composition with Other Skills

- Transcribed interviews → pass to `/podcast` as reference material
- Voice notes → pass to `/explainer` as input content
- Meeting recordings → pass to `baoyu-format-markdown` for cleanup

## Notes

- WAV works without ffmpeg; all other formats require it
- Raw transcript is always preserved before AI polishing
- Results displayed in conversation; Markdown save is optional
- Source: [ListenHub ASR Skill](https://listenhub.ai/docs/zh/skills/asr)
