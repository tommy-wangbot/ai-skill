#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader, PdfWriter

try:
    import pdfplumber  # type: ignore
except Exception:  # pragma: no cover
    pdfplumber = None


def maybe_run_in_skill_venv() -> int | None:
    if os.environ.get("GLM_OCR_PDF_IN_VENV") == "1":
        return None
    venv_root = Path(__file__).resolve().parents[1] / ".venv"
    venv_python = venv_root / "bin" / "python"
    if not venv_python.is_file():
        return None
    if Path(sys.prefix).resolve() == venv_root.resolve():
        return None
    env = os.environ.copy()
    env["GLM_OCR_PDF_IN_VENV"] = "1"
    return subprocess.run(
        [str(venv_python), str(Path(__file__).resolve()), *sys.argv[1:]],
        check=False,
        env=env,
    ).returncode


@dataclass
class PageRange:
    start: int  # 0-based, inclusive
    end: int  # 0-based, inclusive

    @property
    def label(self) -> str:
        if self.start == self.end:
            return f"p{self.start + 1}"
        return f"p{self.start + 1}-{self.end + 1}"


def normalize_text(text: str | None) -> str:
    return (text or "").replace("\x00", "").strip()


def parse_page_ranges(spec: str, total_pages: int) -> list[PageRange]:
    ranges: list[PageRange] = []
    for raw_part in spec.split(","):
        part = raw_part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
        else:
            start = end = int(part)
        if start < 1 or end < 1 or start > total_pages or end > total_pages:
            raise ValueError(f"Page range out of bounds: {part} for {total_pages} pages")
        if end < start:
            raise ValueError(f"Invalid descending page range: {part}")
        ranges.append(PageRange(start - 1, end - 1))
    if not ranges:
        raise ValueError("No valid page ranges provided")
    return ranges


def write_json(data: object, output: Path | None) -> None:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    if output is None:
        print(payload)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload, encoding="utf-8")
    print(output)


def metadata_to_dict(reader: PdfReader) -> dict[str, str]:
    meta = reader.metadata or {}
    result: dict[str, str] = {}
    for key, value in meta.items():
        cleaned = str(value).strip() if value is not None else ""
        if cleaned:
            result[str(key)] = cleaned
    return result


def safe_get_object(value):
    try:
        return value.get_object()
    except Exception:
        return value


def get_full_annotation_field_id(annotation) -> str | None:
    components: list[str] = []
    current = annotation
    while current is not None:
        obj = safe_get_object(current)
        field_name = obj.get("/T")
        if field_name:
            components.append(str(field_name))
        current = obj.get("/Parent")
    return ".".join(reversed(components)) if components else None


def make_field_dict(field, field_id: str) -> dict:
    field_dict = {"field_id": field_id}
    ft = field.get("/FT")
    if ft == "/Tx":
        field_dict["type"] = "text"
    elif ft == "/Btn":
        states = field.get("/_States_", [])
        if field.get("/Kids"):
            field_dict["type"] = "radio_group"
        else:
            field_dict["type"] = "checkbox"
            if len(states) == 2:
                if "/Off" in states:
                    field_dict["checked_value"] = (
                        states[0] if states[0] != "/Off" else states[1]
                    )
                    field_dict["unchecked_value"] = "/Off"
                else:
                    field_dict["checked_value"] = states[0]
                    field_dict["unchecked_value"] = states[1]
    elif ft == "/Ch":
        field_dict["type"] = "choice"
        states = field.get("/_States_", [])
        field_dict["choice_options"] = [
            {"value": state[0], "text": state[1]} for state in states
        ]
    else:
        field_dict["type"] = f"unknown ({ft})"
    return field_dict


def get_field_info(reader: PdfReader) -> list[dict]:
    fields = reader.get_fields() or {}
    field_info_by_id: dict[str, dict] = {}
    possible_radio_names: set[str] = set()

    for field_id, raw_field in fields.items():
        field = safe_get_object(raw_field)
        if field.get("/Kids"):
            if field.get("/FT") == "/Btn":
                possible_radio_names.add(field_id)
            continue
        field_info_by_id[field_id] = make_field_dict(field, field_id)

    radio_fields_by_id: dict[str, dict] = {}
    for page_index, page in enumerate(reader.pages):
        annotations = page.get("/Annots", [])
        for raw_ann in annotations:
            ann = safe_get_object(raw_ann)
            field_id = get_full_annotation_field_id(ann)
            if not field_id:
                continue
            if field_id in field_info_by_id:
                field_info_by_id[field_id]["page"] = page_index + 1
                field_info_by_id[field_id]["rect"] = ann.get("/Rect")
            elif field_id in possible_radio_names:
                try:
                    on_values = [v for v in ann["/AP"]["/N"] if v != "/Off"]
                except Exception:
                    continue
                if len(on_values) == 1:
                    radio = radio_fields_by_id.setdefault(
                        field_id,
                        {
                            "field_id": field_id,
                            "type": "radio_group",
                            "page": page_index + 1,
                            "radio_options": [],
                        },
                    )
                    radio["radio_options"].append(
                        {"value": on_values[0], "rect": ann.get("/Rect")}
                    )

    fields_with_location = [
        field_info for field_info in field_info_by_id.values() if "page" in field_info
    ]

    def sort_key(field: dict) -> list:
        if "radio_options" in field and field["radio_options"]:
            rect = field["radio_options"][0]["rect"] or [0, 0, 0, 0]
        else:
            rect = field.get("rect") or [0, 0, 0, 0]
        return [field.get("page", 0), -rect[1], rect[0]]

    result = fields_with_location + list(radio_fields_by_id.values())
    result.sort(key=sort_key)
    return result


def validation_error_for_field_value(field_info: dict, field_value: str) -> str | None:
    field_type = field_info["type"]
    field_id = field_info["field_id"]
    if field_type == "checkbox":
        checked_val = field_info.get("checked_value")
        unchecked_val = field_info.get("unchecked_value")
        if field_value not in {checked_val, unchecked_val}:
            return (
                f'Invalid value "{field_value}" for checkbox "{field_id}". '
                f'Use "{checked_val}" or "{unchecked_val}".'
            )
    elif field_type == "radio_group":
        option_values = [opt["value"] for opt in field_info.get("radio_options", [])]
        if field_value not in option_values:
            return (
                f'Invalid value "{field_value}" for radio group "{field_id}". '
                f"Valid values: {option_values}"
            )
    elif field_type == "choice":
        choice_values = [opt["value"] for opt in field_info.get("choice_options", [])]
        if field_value not in choice_values:
            return (
                f'Invalid value "{field_value}" for choice "{field_id}". '
                f"Valid values: {choice_values}"
            )
    return None


def cmd_probe(args: argparse.Namespace) -> int:
    reader = PdfReader(str(args.input_pdf))
    page_count = len(reader.pages)
    sample_count = min(page_count, args.max_pages)
    page_summaries = []
    text_pages = 0
    total_chars = 0

    for page_index in range(sample_count):
        text = normalize_text(reader.pages[page_index].extract_text())
        char_count = len(text)
        has_text = char_count >= args.min_chars
        text_pages += int(has_text)
        total_chars += char_count
        page_summaries.append(
            {
                "page": page_index + 1,
                "char_count": char_count,
                "has_extractable_text": has_text,
            }
        )

    ratio = (text_pages / sample_count) if sample_count else 0.0
    if sample_count == 0:
        recommended_mode = "native"
        reason = "empty document"
    elif text_pages == 0 or ratio < 0.3 or total_chars < args.min_chars:
        recommended_mode = "ocr"
        reason = "little or no extractable text found in sampled pages"
    elif ratio < 0.9:
        recommended_mode = "mixed"
        reason = "some pages have text, some pages may still need OCR"
    else:
        recommended_mode = "native"
        reason = "usable text layer detected"

    data = {
        "input_pdf": str(args.input_pdf),
        "page_count": page_count,
        "sampled_pages": sample_count,
        "extractable_text_pages": text_pages,
        "total_sampled_chars": total_chars,
        "has_fillable_fields": bool(reader.get_fields()),
        "metadata": metadata_to_dict(reader),
        "recommended_mode": recommended_mode,
        "reason": reason,
        "pages": page_summaries,
    }
    write_json(data, args.output)
    return 0


def cmd_extract_text(args: argparse.Namespace) -> int:
    reader = PdfReader(str(args.input_pdf))
    parts = []
    for index, page in enumerate(reader.pages, start=1):
        text = normalize_text(page.extract_text())
        parts.append(f"--- Page {index} ---\n{text}")
    payload = "\n\n".join(parts).strip() + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(args.output)
    else:
        sys.stdout.write(payload)
    return 0


def cmd_extract_tables(args: argparse.Namespace) -> int:
    if pdfplumber is None:
        reexec_code = maybe_run_in_skill_venv()
        if reexec_code is not None:
            return reexec_code
        print(
            "pdfplumber is not installed for this Python. Install it in a venv or use OCR fallback.",
            file=sys.stderr,
        )
        return 2
    rows = []
    with pdfplumber.open(str(args.input_pdf)) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table_index, table in enumerate(tables, start=1):
                rows.append(
                    {
                        "page": page_number,
                        "table_index": table_index,
                        "rows": table,
                    }
                )
    write_json(rows, args.output)
    return 0


def iter_selected_pages(reader: PdfReader, ranges: Iterable[PageRange]):
    for page_range in ranges:
        writer = PdfWriter()
        for page_index in range(page_range.start, page_range.end + 1):
            writer.add_page(reader.pages[page_index])
        yield page_range, writer


def cmd_merge(args: argparse.Namespace) -> int:
    writer = PdfWriter()
    for pdf_path in args.input_pdfs:
        writer.append(str(pdf_path))
    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with args.output_pdf.open("wb") as handle:
        writer.write(handle)
    print(args.output_pdf)
    return 0


def cmd_split(args: argparse.Namespace) -> int:
    reader = PdfReader(str(args.input_pdf))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.one_per_page:
        ranges = [PageRange(i, i) for i in range(len(reader.pages))]
    else:
        ranges = parse_page_ranges(args.ranges, len(reader.pages))

    stem = args.input_pdf.stem
    for page_range, writer in iter_selected_pages(reader, ranges):
        output = args.output_dir / f"{stem}_{page_range.label}.pdf"
        with output.open("wb") as handle:
            writer.write(handle)
        print(output)
    return 0


def cmd_rotate(args: argparse.Namespace) -> int:
    reader = PdfReader(str(args.input_pdf))
    writer = PdfWriter()
    selected = parse_page_ranges(args.pages, len(reader.pages))
    selected_pages = {
        page_index
        for page_range in selected
        for page_index in range(page_range.start, page_range.end + 1)
    }
    for page_index, page in enumerate(reader.pages):
        if page_index in selected_pages:
            page.rotate(args.degrees)
        writer.add_page(page)
    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with args.output_pdf.open("wb") as handle:
        writer.write(handle)
    print(args.output_pdf)
    return 0


def cmd_inspect_forms(args: argparse.Namespace) -> int:
    reader = PdfReader(str(args.input_pdf))
    write_json(get_field_info(reader), args.output)
    return 0


def cmd_fill_forms(args: argparse.Namespace) -> int:
    reader = PdfReader(str(args.input_pdf))
    field_info = get_field_info(reader)
    fields_by_id = {field["field_id"]: field for field in field_info}
    requested_fields = json.loads(args.field_values_json.read_text(encoding="utf-8"))
    fields_by_page: dict[int, dict[str, str]] = {}
    errors = []

    for item in requested_fields:
        field_id = item["field_id"]
        value = item.get("value")
        if value is None:
            continue
        existing = fields_by_id.get(field_id)
        if existing is None:
            errors.append(f"Unknown field_id: {field_id}")
            continue
        if item.get("page") != existing.get("page"):
            errors.append(
                f'Incorrect page for "{field_id}": got {item.get("page")}, '
                f'expected {existing.get("page")}'
            )
            continue
        validation_error = validation_error_for_field_value(existing, value)
        if validation_error:
            errors.append(validation_error)
            continue
        fields_by_page.setdefault(existing["page"], {})[field_id] = value

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    writer = PdfWriter(clone_from=reader)
    for page_number, values in fields_by_page.items():
        writer.update_page_form_field_values(
            writer.pages[page_number - 1], values, auto_regenerate=False
        )
    writer.set_need_appearances_writer(True)
    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with args.output_pdf.open("wb") as handle:
        writer.write(handle)
    print(args.output_pdf)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Native PDF helpers with OCR routing.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    probe = subparsers.add_parser("probe", help="Decide whether a PDF needs OCR.")
    probe.add_argument("input_pdf", type=Path)
    probe.add_argument("--output", type=Path)
    probe.add_argument("--max-pages", type=int, default=10)
    probe.add_argument("--min-chars", type=int, default=20)
    probe.set_defaults(func=cmd_probe)

    extract_text = subparsers.add_parser("extract-text", help="Extract native PDF text.")
    extract_text.add_argument("input_pdf", type=Path)
    extract_text.add_argument("--output", type=Path)
    extract_text.set_defaults(func=cmd_extract_text)

    extract_tables = subparsers.add_parser(
        "extract-tables", help="Extract native PDF tables with pdfplumber."
    )
    extract_tables.add_argument("input_pdf", type=Path)
    extract_tables.add_argument("--output", type=Path)
    extract_tables.set_defaults(func=cmd_extract_tables)

    merge = subparsers.add_parser("merge", help="Merge multiple PDFs.")
    merge.add_argument("output_pdf", type=Path)
    merge.add_argument("input_pdfs", nargs="+", type=Path)
    merge.set_defaults(func=cmd_merge)

    split = subparsers.add_parser("split", help="Split a PDF by page ranges.")
    split.add_argument("input_pdf", type=Path)
    split.add_argument("--output-dir", type=Path, required=True)
    split.add_argument("--ranges", default="1")
    split.add_argument("--one-per-page", action="store_true")
    split.set_defaults(func=cmd_split)

    rotate = subparsers.add_parser("rotate", help="Rotate selected pages.")
    rotate.add_argument("input_pdf", type=Path)
    rotate.add_argument("output_pdf", type=Path)
    rotate.add_argument("--pages", required=True)
    rotate.add_argument("--degrees", type=int, choices=[90, 180, 270], required=True)
    rotate.set_defaults(func=cmd_rotate)

    inspect_forms = subparsers.add_parser(
        "inspect-forms", help="List fillable form fields as JSON."
    )
    inspect_forms.add_argument("input_pdf", type=Path)
    inspect_forms.add_argument("--output", type=Path)
    inspect_forms.set_defaults(func=cmd_inspect_forms)

    fill_forms = subparsers.add_parser(
        "fill-forms", help="Fill a PDF using a field_values JSON payload."
    )
    fill_forms.add_argument("input_pdf", type=Path)
    fill_forms.add_argument("field_values_json", type=Path)
    fill_forms.add_argument("output_pdf", type=Path)
    fill_forms.set_defaults(func=cmd_fill_forms)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
