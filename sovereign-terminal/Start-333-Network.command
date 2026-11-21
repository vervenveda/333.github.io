#!/bin/zsh
set -euo pipefail
umask 077
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$ROOT"
command -v node >/dev/null 2>&1 || { echo "WITHHOLD: Node.js is required."; exit 1; }
node --version
exec node "$HERE/333-network-terminal.mjs"
