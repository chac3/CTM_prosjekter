#!/usr/bin/env python3
"""Convert ordinary Python code blocks in Quarto files to runnable Pyodide blocks.

This is a conservative post-processor for QMD files produced by an IPYNB-to-QMD
migration. It does not execute code or invent tests. It changes code-fence
engines and optionally adds cell options understood by many live-code filters.

Examples
--------
Dry run using the common coatless-quarto engine name::

    python3 tools/qmd_python_to_pyodide.py projects-migrated --dry-run

Convert in place and keep .bak files::

    python3 tools/qmd_python_to_pyodide.py projects-migrated \
        --engine pyodide-python --backup

For an extension with a different engine name::

    python3 tools/qmd_python_to_pyodide.py projects-migrated \
        --engine pyodide-interaktiv

Always inspect one rendered page before converting the entire tree.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

VERSION = "0.2.0"

OPEN_FENCE_RE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})"
    r"\{(?P<header>[^}]*)\}[ \t]*$"
)

# A plain markdown fence such as ```python is supported too.
PLAIN_FENCE_RE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})"
    r"(?P<language>python|python3|py)[ \t]*$",
    re.I,
)

INCOMPLETE_PATTERNS = [
    re.compile(r"(?m)^\s*\.\.\.\s*(?:#.*)?$"),
    re.compile(r"(?m)=\s*\.\.\.\s*(?:#.*)?$"),
    re.compile(r"\breturn\s+\.\.\."),
    re.compile(r"\braise\s+NotImplementedError\b"),
    re.compile(r"\bYOUR_CODE_HERE\b", re.I),
    re.compile(r"\bTODO\b", re.I),
]

DANGEROUS_PATTERNS = {
    "shell command": re.compile(r"(?m)^\s*!|\bsubprocess\b|\bos\.system\s*\("),
    "local filesystem": re.compile(r"\bopen\s*\(|\bPath\s*\(|\bpathlib\b|\bshutil\b"),
    "network access": re.compile(r"\brequests\b|\burllib\b|\bsocket\b|\bhttpx\b"),
    "package installation": re.compile(r"(?m)^\s*%?pip\s+install\b|\bsubprocess.*pip\b"),
    "notebook magic": re.compile(r"(?m)^\s*[%]{1,2}[A-Za-z]"),
}


@dataclass
class FileReport:
    path: str
    changed: bool = False
    converted_blocks: int = 0
    skipped_blocks: int = 0
    incomplete_blocks: int = 0
    unsafe_blocks: int = 0
    already_pyodide_blocks: int = 0
    warnings: list[str] | None = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


def split_header(header: str) -> tuple[str, str]:
    """Return (engine, remaining header text)."""
    stripped = header.strip()
    if not stripped:
        return "", ""
    match = re.match(r"(?P<engine>[A-Za-z0-9_.+-]+)(?P<rest>.*)$", stripped)
    if not match:
        return stripped, ""
    return match.group("engine"), match.group("rest")


def replace_engine(header: str, engine: str) -> str:
    _, rest = split_header(header)
    return engine + rest


def is_python_engine(engine: str) -> bool:
    return engine.lower() in {"python", "python3", "py"}


def is_pyodide_engine(engine: str) -> bool:
    value = engine.lower()
    return "pyodide" in value


def contains_incomplete(code: str) -> bool:
    return any(pattern.search(code) for pattern in INCOMPLETE_PATTERNS)


def unsafe_reasons(code: str) -> list[str]:
    return [name for name, pattern in DANGEROUS_PATTERNS.items() if pattern.search(code)]


def closing_fence(line: str, opening_fence: str, indent: str) -> bool:
    char = opening_fence[0]
    length = len(opening_fence)
    return bool(re.match(rf"^{re.escape(indent)}{re.escape(char)}{{{length},}}\s*$", line))


def option_lines(existing_code_lines: list[str], args: argparse.Namespace, incomplete: bool) -> list[str]:
    """Construct optional #| lines without duplicating existing options."""
    existing = "\n".join(existing_code_lines[:20])
    additions: list[str] = []

    def add(name: str, value: str) -> None:
        if not re.search(rf"(?m)^\s*#\|\s*{re.escape(name)}\s*:", existing):
            additions.append(f"#| {name}: {value}")

    if args.editable is not None:
        add("edit", "true" if args.editable else "false")
    if args.run_button is not None:
        add("runbutton", "true" if args.run_button else "false")
    if args.autorun is not None:
        requested = args.autorun and not incomplete
        add("autorun", "true" if requested else "false")
    if args.persist is not None:
        add("persist", "true" if args.persist else "false")
    return additions


def convert_text(text: str, path: Path, args: argparse.Namespace) -> tuple[str, FileReport]:
    lines = text.splitlines()
    output: list[str] = []
    report = FileReport(path=str(path))
    index = 0

    while index < len(lines):
        line = lines[index]
        match = OPEN_FENCE_RE.match(line)
        plain = PLAIN_FENCE_RE.match(line)

        if not match and not plain:
            output.append(line)
            index += 1
            continue

        if match:
            indent = match.group("indent")
            fence = match.group("fence")
            header = match.group("header")
            engine, _ = split_header(header)
        else:
            indent = plain.group("indent")
            fence = plain.group("fence")
            header = plain.group("language")
            engine = header

        # Capture through the matching closing fence.
        block = [line]
        cursor = index + 1
        while cursor < len(lines):
            block.append(lines[cursor])
            if closing_fence(lines[cursor], fence, indent):
                break
            cursor += 1

        if cursor >= len(lines):
            report.warnings.append(f"Unclosed code fence beginning at line {index + 1}.")
            output.extend(block)
            index = cursor
            continue

        code_lines = block[1:-1]
        code = "\n".join(code_lines)

        if is_pyodide_engine(engine):
            report.already_pyodide_blocks += 1
            output.extend(block)
            index = cursor + 1
            continue

        if not is_python_engine(engine):
            output.extend(block)
            index = cursor + 1
            continue

        incomplete = contains_incomplete(code)
        reasons = unsafe_reasons(code)
        if incomplete:
            report.incomplete_blocks += 1
        if reasons:
            report.unsafe_blocks += 1

        skip = False
        if incomplete and args.skip_incomplete:
            skip = True
            report.warnings.append(
                f"Line {index + 1}: skipped incomplete Python block."
            )
        if reasons and args.skip_unsafe:
            skip = True
            report.warnings.append(
                f"Line {index + 1}: skipped block requiring {', '.join(reasons)}."
            )

        if skip:
            report.skipped_blocks += 1
            output.extend(block)
            index = cursor + 1
            continue

        # Preserve labels/classes/options after the engine name in {...}.
        new_header = replace_engine(header, args.engine)
        new_open = f"{indent}{fence}{{{new_header}}}"
        additions = option_lines(code_lines, args, incomplete)

        output.append(new_open)
        output.extend(additions)
        output.extend(code_lines)
        output.append(block[-1])
        report.converted_blocks += 1
        report.changed = True
        index = cursor + 1

    result = "\n".join(output)
    if text.endswith("\n"):
        result += "\n"
    return result, report


def qmd_files(root: Path, recursive: bool, include_hidden: bool) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() == ".qmd" else []
    iterator = root.rglob("*.qmd") if recursive else root.glob("*.qmd")
    files = []
    for path in iterator:
        relative = path.relative_to(root)
        if not include_hidden and any(part.startswith(".") for part in relative.parts):
            continue
        if "_site" in path.parts or ".quarto" in path.parts:
            continue
        files.append(path)
    return sorted(files)


def write_report(path: Path, reports: Iterable[FileReport]) -> None:
    reports = list(reports)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".json":
        path.write_text(
            json.dumps([asdict(item) for item in reports], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return
    fields = [
        "path", "changed", "converted_blocks", "skipped_blocks",
        "incomplete_blocks", "unsafe_blocks", "already_pyodide_blocks", "warnings",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in reports:
            row = asdict(item)
            row["warnings"] = " | ".join(item.warnings or [])
            writer.writerow(row)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Python code fences in QMD files to runnable Pyodide fences.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("source", type=Path, help="QMD file or directory.")
    parser.add_argument(
        "--engine", default="pyodide-python",
        help="Target Quarto code-fence engine. Inspect your extension documentation first.",
    )
    parser.add_argument("--recursive", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--include-hidden", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup", action="store_true", help="Create .bak before changing each file.")
    parser.add_argument("--backup-suffix", default=".bak")
    parser.add_argument("--skip-incomplete", action="store_true",
                        help="Leave blocks with ..., TODO or NotImplementedError unchanged.")
    parser.add_argument("--skip-unsafe", action=argparse.BooleanOptionalAction, default=True,
                        help="Leave shell, filesystem, network, pip and notebook-magic blocks unchanged.")
    parser.add_argument("--editable", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--run-button", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--autorun", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--persist", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--report", type=Path, default=Path("migration/pyodide-conversion.csv"))
    parser.add_argument("--version", action="version", version=VERSION)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source = args.source.expanduser().resolve()
    if not source.exists():
        print(f"ERROR: source does not exist: {source}", file=sys.stderr)
        return 2

    files = qmd_files(source, args.recursive, args.include_hidden)
    if not files:
        print(f"No QMD files found under {source}", file=sys.stderr)
        return 1

    reports: list[FileReport] = []
    print(f"Engine: {args.engine}")
    print(f"Found {len(files)} QMD file(s).")

    for number, path in enumerate(files, start=1):
        original = path.read_text(encoding="utf-8")
        converted, report = convert_text(original, path, args)
        reports.append(report)
        print(
            f"[{number:>4}/{len(files)}] {path}: "
            f"converted={report.converted_blocks}, "
            f"skipped={report.skipped_blocks}, "
            f"incomplete={report.incomplete_blocks}, "
            f"unsafe={report.unsafe_blocks}"
        )
        if report.changed and not args.dry_run:
            if args.backup:
                backup = path.with_name(path.name + args.backup_suffix)
                if not backup.exists():
                    shutil.copy2(path, backup)
            path.write_text(converted, encoding="utf-8")

    if not args.dry_run:
        write_report(args.report, reports)

    changed = sum(item.changed for item in reports)
    converted = sum(item.converted_blocks for item in reports)
    skipped = sum(item.skipped_blocks for item in reports)
    print(f"Done. changed_files={changed}, converted_blocks={converted}, skipped_blocks={skipped}")
    if args.dry_run:
        print("Dry run: no files were changed and no report was written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
