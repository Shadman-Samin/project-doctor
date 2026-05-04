"""Check for code formatting and linting configurations."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class CheckResult:
    status: str
    message: str
    suggestions: list[str] = field(default_factory=list)


def check(path: str) -> CheckResult:
    files = [f.lower() for f in os.listdir(path)] if os.path.isdir(path) else []
    
    formatters = [
        ".pre-commit-config.yaml",
        ".flake8",
        ".eslintrc.js",
        ".eslintrc.json",
        ".prettierrc",
    ]
    
    found = [f for f in formatters if f in files]
    
    # Also check pyproject.toml for tool configs like ruff, black, isort
    has_pyproject_config = False
    pyproject_path = os.path.join(path, "pyproject.toml")
    if os.path.isfile(pyproject_path):
        with open(pyproject_path, encoding="utf-8", errors="replace") as f:
            content = f.read()
            if any(tool in content for tool in ["[tool.ruff]", "[tool.black]", "[tool.isort]"]):
                has_pyproject_config = True
                
    if found or has_pyproject_config:
        return CheckResult(status="ok", message="Formatter/Linter config found")
        
    return CheckResult(
        status="warn",
        message="No formatter or linter config found",
        suggestions=[
            "Add a formatter like Black, Ruff, or Prettier to maintain consistent code style.",
            "Consider setting up pre-commit with .pre-commit-config.yaml."
        ],
    )
