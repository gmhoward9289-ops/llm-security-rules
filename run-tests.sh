#!/usr/bin/env bash
# Run the full rule test suite: every rule's pass/fail fixtures via semgrep --test.
set -euo pipefail
cd "$(dirname "$0")"

SEMGREP="${SEMGREP:-semgrep}"
if ! command -v "$SEMGREP" >/dev/null 2>&1; then
  echo "error: semgrep not found. Install with: pip install semgrep (or set SEMGREP=/path/to/semgrep)" >&2
  exit 1
fi

"$SEMGREP" --test rules/
