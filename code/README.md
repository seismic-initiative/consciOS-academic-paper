# ConsciOS Demo: Hierarchical Controller Benchmark

Minimal ablations for the ConsciOS architecture:
- Flat agent vs Hierarchical (Echo/Super/Meta)
- Resonance Engine selection (β/α sweeps)
- Cumulative coherence gating (FREQ on/off)
- EGS‑like intrinsic shaping on/off

## Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

## Run
# Flat baseline
python -m agents.flat_agent --episodes 200 --seed 1
# Hierarchical
python -m agents.hier_agent --episodes 200 --seed 1 --beta 1.0 --alpha 0.5 --freq_on true --egs_on true

## Plots
python -m plots.plot_traces

## Ablations (β/α sweeps)
# Generate β×α logs and per‑run plots, then summarize into heatmaps
PYTHONPATH=code python -m ablate.run_ablation
PYTHONPATH=code python -m ablate.summarize_ablation

# Outputs:
# logs/hier_b{beta}_a{alpha}.csv
# plots/hier_b{beta}_a{alpha}_reward.png, plots/hier_b{beta}_a{alpha}_pos.png
# plots/ablation_summary.csv and heatmaps under plots/

## Outputs
- logs/: selection traces, coherence scores, FREQ timeline
- plots/: hold_time vs policy_entropy, adaptation_latency, OA vs FREQ

## Notes
Default coherence: log‑evidence proxy; KLD/cosine alternatives available in coherence/.


