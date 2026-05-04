"""Check for .editorconfig."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class CheckResult:
    status: str
    message: str
    suggestions: list[str] = field(default_factory=list)


def check(path: str) -> CheckResult:
    editorconfig_path = os.path.join(path, ".editorconfig")
    
    if os.path.isfile(editorconfig_path):
        return CheckResult(status="ok", message=".editorconfig found")
        
    return CheckResult(
        status="warn",
        message=".editorconfig missing",
        suggestions=[
            "Add an .editorconfig file to ensure consistent whitespace and indent styles across different IDEs."
        ],
    )
