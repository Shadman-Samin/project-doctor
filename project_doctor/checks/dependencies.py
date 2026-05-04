"""Check for dependency management files."""

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
    
    dep_files = [
        "requirements.txt",
        "pipfile",
        "poetry.lock",
        "package.json",
        "cargo.toml",
        "go.mod",
        "gemfile",
    ]
    
    found = [f for f in dep_files if f in files]
    
    # Also check pyproject.toml for dependencies
    pyproject_path = os.path.join(path, "pyproject.toml")
    has_pyproject_deps = False
    if os.path.isfile(pyproject_path):
        with open(pyproject_path, encoding="utf-8", errors="replace") as f:
            content = f.read()
            if "dependencies" in content or "tool.poetry.dependencies" in content:
                has_pyproject_deps = True
                
    if found or has_pyproject_deps:
        return CheckResult(status="ok", message="Dependency management found")
        
    return CheckResult(
        status="fail",
        message="No dependency management found",
        suggestions=[
            "Specify your project dependencies so others can run it.",
            "E.g., create a requirements.txt or use pyproject.toml / Poetry."
        ],
    )
