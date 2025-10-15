#!/usr/bin/env bash
set -euo pipefail
if ! command -v mmdc >/dev/null 2>&1; then
  echo "mmdc not found. Install with: npm i -g @mermaid-js/mermaid-cli" >&2
  exit 1
fi
mkdir -p preprint/figures
for f in mermaid/*.mmd; do
  base=$(basename "$f" .mmd)
  mmdc -i "$f" -o "preprint/figures/${base}.png" -b transparent
  echo "Rendered $base.png"
done
