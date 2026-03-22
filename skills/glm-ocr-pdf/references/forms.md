# PDF Forms

Use this reference when the user wants to inspect or fill a PDF form.

## Order of operations

1. Run `scripts/pdf_native.py probe <file.pdf>` and check `has_fillable_fields`.
2. If the PDF has fillable fields, use native form inspection and filling.
3. If the PDF does not have fillable fields, treat it as a scanned or visually positioned form:
   - OCR it with `scripts/run_glmocr.py` if content understanding is needed.
   - Then create a new filled artifact or overlay instead of pretending the original PDF is editable.

## Fillable forms

Inspect fields:

```bash
python3 scripts/pdf_native.py inspect-forms /absolute/path/to/form.pdf --output /absolute/path/to/field-info.json
```

The JSON includes:
- `field_id`
- `page`
- `type`
- `rect`
- checkbox/radio/choice options when available

Prepare `field_values.json` like this:

```json
[
  {
    "field_id": "name.last",
    "page": 1,
    "value": "Simpson"
  }
]
```

Fill the PDF:

```bash
python3 scripts/pdf_native.py fill-forms /absolute/path/to/form.pdf /absolute/path/to/field_values.json /absolute/path/to/filled.pdf
```

## Non-fillable forms

- Do not use `fill-forms`.
- Use OCR only to understand labels, values, and layout.
- If the user wants a completed deliverable, create a new PDF, an annotated copy, or another output format.
