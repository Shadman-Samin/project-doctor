"""Check for contributing guidelines and community health files."""

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
    
    has_contributing = any("contributing" in f and f.endswith(".md") for f in files)
    has_coc = any("code_of_conduct" in f and f.endswith(".md") for f in files)
    
    github_dir = os.path.join(path, ".github")
    has_issue_template = False
    if os.path.isdir(github_dir):
        github_files = os.listdir(github_dir)
        if "ISSUE_TEMPLATE" in github_files or any("issue_template" in f.lower() for f in github_files):
            has_issue_template = True
            
    if has_contributing and has_coc and has_issue_template:
        return CheckResult(status="ok", message="Community health files found")
        
    missing = []
    if not has_contributing:
        missing.append("CONTRIBUTING.md")
    if not has_coc:
        missing.append("CODE_OF_CONDUCT.md")
    if not has_issue_template:
        missing.append("Issue Templates")
        
    return CheckResult(
        status="warn",
        message="Missing community health files",
        suggestions=[f"Consider adding {', '.join(missing)} to encourage community contributions."],
    )
