#!/usr/bin/env bash
# Cross-platform launcher (macOS / Linux / Windows Git Bash)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Auto-detect venv Python: Windows layout vs Unix layout
for candidate in \
    "$ROOT_DIR/.venv/bin/python" \
    "$ROOT_DIR/.venv/Scripts/python.exe" \
    "$ROOT_DIR/.venv/Scripts/python"; do
    if [ -f "$candidate" ]; then
        exec "$candidate" "$ROOT_DIR/run.py" "$@"
    fi
done

echo "ERROR: venv python not found in $ROOT_DIR/.venv" >&2
exit 1
