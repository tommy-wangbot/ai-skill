# OCR + PDF Workflow

Use this reference after OCR has already been identified as necessary.

## 1. Native-text vs scanned PDF

- Native-text PDF:
  - Prefer `pypdf`, `pdfplumber`, `pdftotext`, or form-aware tools.
  - Skip GLM-OCR unless the user explicitly wants OCR-style Markdown/layout blocks.
- Scanned or image-only PDF:
  - Run `scripts/run_glmocr.py` first.
  - Review both Markdown and JSON outputs before cleanup.

## 2. Tables

- First inspect the generated Markdown to see whether the table is already usable.
- If the user needs structured recovery or row/column cleanup, inspect the JSON blocks.
- Table-heavy scans may still need manual normalization after OCR.
- Preserve the raw OCR output before rewriting table content.

## 3. Forms

- Fillable AcroForm / text PDF:
  - Use PDF-native form tools instead of OCR.
- Scanned form:
  - Use GLM-OCR to read field labels, values, and layout.
  - If the user wants a completed form, generate a new filled artifact or overlay; do not promise preservation of editable fields in the original scan.

## 4. Merge / split / rotate

- These operations usually do not need OCR.
- Only OCR first when the user also needs content extraction or interpretation.

## 5. Recommended artifact flow

1. Keep the original PDF unchanged.
2. Run GLM-OCR into a dedicated output directory.
3. Read `<stem>.md` for quick validation.
4. Read `<stem>.json` for region-aware follow-up tasks.
5. Write any cleaned tables, summaries, or reconstructed forms as separate outputs.
