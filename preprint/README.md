# ConsciOS v1.0 — Preprint Packaging

This folder contains assets and instructions to build and submit the preprint to arXiv and ResearchGate.

## Files
- paper.md — main manuscript
- preprint/figures/*.png — rendered figures (from Mermaid sources in /mermaid)
- scripts/render_mermaid.sh — render helper (uses Mermaid CLI `mmdc`)
- scripts/build_pdf.sh — optional Pandoc-based PDF build (IEEE-like)

## arXiv submission
1. Render figures: `./scripts/render_mermaid.sh`
2. Verify images exist at `preprint/figures/`
3. Upload to arXiv: `paper.md`, the `preprint/figures` directory, and a `LICENSE`.
   - Note: arXiv accepts PDF or source; if using Markdown, convert to PDF with Pandoc below.

## ResearchGate
Upload the compiled PDF and optionally attach the source repository link.

## Build PDF (optional)
Requires Pandoc and LaTeX (TinyTeX/MacTeX).

```bash
brew install pandoc
# For LaTeX: brew install --cask mactex-no-gui  # or TinyTeX via tlmgr
./scripts/build_pdf.sh
```

