---
name: glm-ocr-pdf
description: Use local PDF-native tools plus the local GLM-OCR install on this machine to work with PDF files. Trigger when the user asks for PDF reading, text extraction, table extraction, form inspection or filling, merge, split, rotate, or OCR on scanned/image-only PDFs. Route native-text PDFs to `scripts/pdf_native.py` first, and only use GLM-OCR when the PDF has no reliable text layer or the user explicitly needs OCR-style output.
---

# GLM OCR PDF

## When to use
- Any PDF task where the agent needs to decide between native PDF handling and OCR.
- Scanned or image-only PDFs where text cannot be selected.
- Screenshots, camera photos, or rasterized pages that need Markdown/JSON output.
- Table extraction from scanned PDFs before downstream cleanup.
- Reading or understanding a scanned form before rewriting or reconstructing it.
- Native PDF tasks like merge, split, rotate, text extraction, and fillable form inspection.

## When not to use
- Non-PDF document tasks where no PDF or scanned-image workflow is involved.
- Cases where the user explicitly needs another format workflow first, such as DOCX editing before PDF export.
- Do not force GLM-OCR on PDFs that already have a clean text layer.

## Decision rule
1. Run `python3 scripts/pdf_native.py probe <file.pdf>` when the input is a PDF.
2. If `recommended_mode` is `native`, use `scripts/pdf_native.py` and skip OCR.
3. If `recommended_mode` is `ocr` or the PDF is image-only, run `scripts/run_glmocr.py`.
4. If `recommended_mode` is `mixed`, use judgment page by page. Prefer native extraction first, OCR only where extraction is broken.
5. Review OCR Markdown/JSON before any cleanup, summarization, or table reshaping.
6. For table/form follow-up work, read [references/pdf-workflow.md](references/pdf-workflow.md) and [references/forms.md](references/forms.md) when relevant.

## Quick start
Probe a PDF first:

```bash
python3 scripts/pdf_native.py probe /absolute/path/to/input.pdf --output /absolute/path/to/probe.json
```

Run native PDF text extraction:

```bash
python3 scripts/pdf_native.py extract-text /absolute/path/to/input.pdf --output /absolute/path/to/output.txt
```

Run native table extraction:

```bash
python3 scripts/pdf_native.py extract-tables /absolute/path/to/input.pdf --output /absolute/path/to/tables.json
```

Run GLM-OCR with the bundled wrapper when OCR is actually needed:

```bash
python3 scripts/run_glmocr.py /absolute/path/to/input.pdf
```

Choose an explicit output directory when OCR is part of a larger workflow:

```bash
python3 scripts/run_glmocr.py /absolute/path/to/input.pdf --output-dir /absolute/path/to/output
```

The wrapper reuses the local Apple Silicon setup at `/Users/tommy/Documents/codex/GLM-OCR`. If the MLX server is not running, it starts it automatically and waits for health before calling `glmocr parse`.
`extract-tables` will automatically use the skill-local `.venv` when the current Python does not have `pdfplumber`.

## Output expectations
- GLM-OCR writes results under `<output-dir>/<input-stem>/`.
- Expect at least:
  - `<input-stem>.md`
  - `<input-stem>.json`
  - `layout_vis/` images when layout mode is enabled
- Prefer Markdown for human review and JSON for table/region-aware post-processing.

## Workflow
1. Resolve the user's input file(s) and decide whether each file is PDF-native or OCR-first.
2. For PDFs, run `scripts/pdf_native.py probe`.
3. Native tasks:
   - `extract-text` for text-layer PDFs
   - `extract-tables` when `pdfplumber` is available
   - `merge`, `split`, or `rotate` for structural edits
   - `inspect-forms` and `fill-forms` for fillable PDFs
4. OCR tasks:
   - Run `scripts/run_glmocr.py` on scanned PDFs/images
   - Read the generated `.md` first for quality check
   - Read the `.json` for layout-aware follow-up
5. Only after extraction succeeds should you do cleanup, summarization, or rewriting.

## Notes for downstream tasks
- For scanned tables, use the JSON blocks to locate table regions before manual cleanup.
- For native-text tables, try `scripts/pdf_native.py extract-tables` first. If `pdfplumber` is unavailable or the table is image-based, fall back to OCR.
- For scanned forms, use OCR to understand the content, not to "fill" the original PDF structure.
- For fillable PDF forms, use `scripts/pdf_native.py inspect-forms` and `fill-forms`.
- For merge/split/rotate, stay in native mode unless the user separately asks for content extraction.

## Resources
- `scripts/run_glmocr.py`: local wrapper around your Apple Silicon GLM-OCR install.
- `scripts/pdf_native.py`: native PDF probe, text extraction, merge, split, rotate, and form helpers.
- [references/pdf-workflow.md](references/pdf-workflow.md): follow-up guidance for tables, forms, and mixed OCR/PDF tasks.
- [references/forms.md](references/forms.md): fillable vs non-fillable PDF form workflow.
