"""Check for documentation generators and docs/ directory."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class CheckResult:
    status: str
    message: str
    suggestions: list[str] = field(default_factory=list)


def check(path: str) -> CheckResult:
    docs_dir = os.path.join(path, "docs")
    has_docs_dir = os.path.isdir(docs_dir)
    
    files = [f.lower() for f in os.listdir(path)] if os.path.isdir(path) else []
    
    doc_configs = [
        "mkdocs.yml",
        "sphinx",
        "doxygen",
    ]
    
    has_doc_config = any(c in f for f in files for c in doc_configs)
    
    if has_docs_dir or has_doc_config:
        return CheckResult(status="ok", message="Documentation found")
        
    return CheckResult(
        status="warn",
        message="No documentation setup found",
        suggestions=[
            "For larger projects, consider setting up a docs/ folder or a generator like MkDocs or Sphinx."
        ],
    )
