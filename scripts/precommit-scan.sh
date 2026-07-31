#!/usr/bin/env bash
# pre-commit entry point: scan the staged files with this repo's rules.
# Runs from the pre-commit checkout of this repo; consumer files arrive as args.
set -euo pipefail

RULES_DIR="$(cd "$(dirname "$0")/.." && pwd)/rules"

if ! command -v semgrep >/dev/null 2>&1; then
  echo "llm-security-rules: semgrep not found on PATH. Install with: pip install semgrep" >&2
  exit 1
fi

exec semgrep scan --config "$RULES_DIR" --error --quiet "$@"
