#!/usr/bin/env bash
set -euo pipefail
if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not found. Install with: brew install pandoc" >&2
  exit 1
fi
mkdir -p preprint
pandoc \
  --from markdown+smart+implicit_figures+link_attributes \
  --to pdf \
  --pdf-engine=tectonic \
  --template=tex/custom-template.tex \
  --resource-path=. \
  --output preprint/ConsciOS_v1.0_preprint.pdf \
  paper-v1.0.md
echo "Wrote preprint/ConsciOS_v1.0_preprint.pdf"
