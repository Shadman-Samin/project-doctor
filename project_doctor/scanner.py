"""Orchestrates all checks and renders the Rich output."""

from __future__ import annotations

import os
import json
import sys
from dataclasses import dataclass, field
from typing import Callable

from rich.console import Console
from rich.padding import Padding
from rich.rule import Rule
from rich.text import Text

from project_doctor.checks import (
    ci, gitignore, license, readme, structure, tests,
    contributing, formatting, dependencies, documentation, editorconfig, container
)

console = Console()

# ── Icons & colours ──────────────────────────────────────────────────────────
if sys.platform == "win32" and sys.stdout.encoding.lower() != "utf-8":
    _ICON = {"ok": "OK", "warn": "WARN", "fail": "FAIL"}
    _ARROW = "->"
    _RULE_CHAR = "-"
else:
    _ICON = {"ok": "✔", "warn": "⚠", "fail": "✖"}
    _ARROW = "→"
    _RULE_CHAR = "─"

_COLOR = {"ok": "green", "warn": "yellow", "fail": "red"}

# ── Check registry ───────────────────────────────────────────────────────────
# Each tuple: (display label, check module)
_CHECKS: list[tuple[str, object]] = [
    ("README", readme),
    (".gitignore", gitignore),
    ("License", license),
    ("Project Structure", structure),
    ("Tests", tests),
    ("CI / CD", ci),
    ("Contributing", contributing),
    ("Formatting", formatting),
    ("Dependencies", dependencies),
    ("Documentation", documentation),
    ("EditorConfig", editorconfig),
    ("Container", container),
]


@dataclass
class ScanResult:
    label: str
    status: str  # "ok" | "warn" | "fail"
    message: str
    suggestions: list[str] = field(default_factory=list)


def _run_check(label: str, module: object, path: str) -> ScanResult:
    result = module.check(path)  # type: ignore[attr-defined]
    return ScanResult(
        label=label,
        status=result.status,
        message=result.message,
        suggestions=result.suggestions,
    )


def _render_row(result: ScanResult) -> None:
    icon = _ICON.get(result.status, "?")
    color = _COLOR.get(result.status, "white")
    label_text = Text(f"{result.label:<20}", style="bold")
    status_text = Text(f"{icon}  {result.message}", style=color)
    line = Text.assemble(label_text, status_text)
    console.print(line)

    if result.suggestions:
        for suggestion in result.suggestions:
            console.print(
                Text(f"   {_ARROW} {suggestion}", style=f"dim {color}")
            )


def scan(
    path: str,
    strict: bool = False,
    output_format: str = "rich",
    fix: bool = False,
    ignore: list[str] | None = None,
    display_name: str | None = None,
) -> None:
    abs_path = os.path.abspath(path)

    if ignore is None:
        ignore = []
    
    ignore_lower = [i.lower() for i in ignore]
    checks_to_run = [c for c in _CHECKS if c[0].lower() not in ignore_lower]

    if output_format == "rich":
        console.print()
        display = display_name if display_name else abs_path
        console.print(Rule(f"[bold]project-doctor[/bold]  [dim]{display}[/dim]", characters=_RULE_CHAR))
        console.print()

    results: list[ScanResult] = []
    for label, module in checks_to_run:
        result = _run_check(label, module, abs_path)
        
        if fix and result.status in ("warn", "fail") and hasattr(module, "fix"):
            module.fix(abs_path)  # type: ignore
            result = _run_check(label, module, abs_path)

        results.append(result)
        
        if output_format == "rich":
            _render_row(result)

    # ── Summary ──────────────────────────────────────────────────────────────
    total = len(results)
    passed = sum(1 for r in results if r.status == "ok")
    warned = sum(1 for r in results if r.status == "warn")
    failed = sum(1 for r in results if r.status == "fail")

    if output_format == "json":
        output_data = {
            "score": {"passed": passed, "warned": warned, "failed": failed, "total": total},
            "results": [
                {
                    "label": r.label,
                    "status": r.status,
                    "message": r.message,
                    "suggestions": r.suggestions
                }
                for r in results
            ]
        }
        print(json.dumps(output_data, indent=2))
    else:
        console.print()
        console.print(Rule(characters=_RULE_CHAR))

        score_color = "green" if failed == 0 and warned == 0 else ("yellow" if failed == 0 else "red")
        console.print(
            Padding(
                Text.assemble(
                    Text("Score  ", style="bold"),
                    Text(f"{passed}/{total}", style=f"bold {score_color}"),
                    Text(f"  ({passed} passed", style="dim"),
                    Text(f"  {warned} warnings" if warned else "", style="dim yellow"),
                    Text(f"  {failed} failed" if failed else "", style="dim red"),
                    Text(")", style="dim"),
                ),
                (0, 0, 1, 0),
            )
        )

    if strict and failed > 0:
        sys.exit(1)
