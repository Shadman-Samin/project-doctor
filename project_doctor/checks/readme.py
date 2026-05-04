"""Check for README.md presence and required sections."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


REQUIRED_SECTIONS = ["installation", "usage"]


@dataclass
class CheckResult:
    status: str  # "ok" | "warn" | "fail"
    message: str
    suggestions: list[str] = field(default_factory=list)


def check(path: str) -> CheckResult:
    readme_path = os.path.join(path, "README.md")

    if not os.path.isfile(readme_path):
        return CheckResult(
            status="fail",
            message="README.md missing",
            suggestions=[
                "Create a README.md with at minimum: project description, installation steps, and usage examples."
            ],
        )

    with open(readme_path, encoding="utf-8", errors="replace") as f:
        content = f.read().lower()

    missing = [s for s in REQUIRED_SECTIONS if s not in content]

    if missing:
        pretty = ", ".join(s.capitalize() for s in missing)
        return CheckResult(
            status="warn",
            message=f"README exists but missing sections: {pretty}",
            suggestions=[
                f"Add a '## {s.capitalize()}' section to your README.md." for s in missing
            ],
        )

    return CheckResult(status="ok", message="README looks good")
