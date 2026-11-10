"""Fails if any import points outward from a Clean Architecture layer.

Allowed imports (inward only):
  domain          -> domain
  application     -> application, domain
  infrastructure  -> infrastructure, application, domain
  interface       -> everything
Run from the project root:  python scripts/check_dependencies.py
"""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED = {
    "domain": {"domain"},
    "application": {"application", "domain"},
    "infrastructure": {"infrastructure", "application", "domain"},
    "interface": {"interface", "infrastructure", "application", "domain"},
}


def imported_layers(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
        elif isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        for name in names:
            parts = name.split(".")
            if parts[0] == "src" and len(parts) > 1 and parts[1] in ALLOWED:
                yield parts[1]


def main() -> int:
    violations = []
    for layer, allowed in ALLOWED.items():
        for file in (ROOT / "src" / layer).rglob("*.py"):
            for target in imported_layers(file):
                if target not in allowed:
                    violations.append(f"{file.relative_to(ROOT)}: {layer} must not import {target}")
    if violations:
        print("Dependency check FAILED:")
        print("\n".join(violations))
        return 1
    print("Dependency check passed: every import points inward.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
