"""Check for LICENSE file presence."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


LICENSE_FILENAMES = ["LICENSE", "LICENSE.txt", "LICENSE.md", "LICENCE", "LICENCE.txt"]


@dataclass
class CheckResult:
    status: str  # "ok" | "warn" | "fail"
    message: str
    suggestions: list[str] = field(default_factory=list)


def check(path: str) -> CheckResult:
    for name in LICENSE_FILENAMES:
        if os.path.isfile(os.path.join(path, name)):
            return CheckResult(status="ok", message=f"License found ({name})")

    return CheckResult(
        status="fail",
        message="LICENSE missing",
        suggestions=[
            "Add a LICENSE file so users know the terms under which they can use your project.",
            "Choose a license at: https://choosealicense.com",
        ],
    )
