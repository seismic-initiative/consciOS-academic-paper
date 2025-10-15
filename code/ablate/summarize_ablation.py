import csv
import glob
import os
import re
from collections import defaultdict
from typing import Tuple, List

import numpy as np
import matplotlib.pyplot as plt


LOG_PATTERN = re.compile(r"logs/hier_b(?P<beta>[-0-9.]+)_a(?P<alpha>[-0-9.]+)\.csv$")


def load_rows(path: str) -> List[dict]:
	with open(path, "r", encoding="utf-8") as fh:
		reader = csv.DictReader(fh)
		return [row for row in reader]


def metrics_for_rows(rows: List[dict]) -> Tuple[float, float, float]:
	# mean reward
	rewards = [float(r["reward"]) for r in rows]
	mean_reward = float(np.mean(rewards)) if rewards else 0.0
	# alignment rate: action matches ctx sign
	align = [(int(r["action"]) > 0 and int(r["ctx"]) > 0) or (int(r["action"]) < 0 and int(r["ctx"]) < 0) for r in rows]
	alignment_rate = float(np.mean(align)) if align else 0.0
	# position match: closeness to target side (1 if ctx>0 else 0)
	pos = [float(r["norm_pos"]) for r in rows]
	targets = [1.0 if int(r["ctx"]) > 0 else 0.0 for r in rows]
	pos_match = [1.0 - abs(p - t) for p, t in zip(pos, targets)] if rows else []
	mean_pos_match = float(np.mean(pos_match)) if pos_match else 0.0
	return mean_reward, alignment_rate, mean_pos_match


def main():
	files = sorted(glob.glob("logs/hier_b*_a*.csv"))
	results = []
	betas = set()
	alphas = set()
	for f in files:
		m = LOG_PATTERN.match(f)
		if not m:
			continue
		beta = float(m.group("beta"))
		alpha = float(m.group("alpha"))
		betas.add(beta)
		alphas.add(alpha)
		rows = load_rows(f)
		mean_reward, alignment_rate, mean_pos_match = metrics_for_rows(rows)
		results.append((beta, alpha, mean_reward, alignment_rate, mean_pos_match))

	betas = sorted(betas)
	alphas = sorted(alphas)
	# save CSV summary
	os.makedirs("plots", exist_ok=True)
	csv_path = "plots/ablation_summary.csv"
	with open(csv_path, "w", encoding="utf-8", newline="") as fh:
		w = csv.writer(fh)
		w.writerow(["beta", "alpha", "mean_reward", "alignment_rate", "mean_pos_match"])
		for row in sorted(results):
			w.writerow(row)

	# build grids
	reward_grid = np.full((len(betas), len(alphas)), np.nan)
	align_grid = np.full((len(betas), len(alphas)), np.nan)
	pos_grid = np.full((len(betas), len(alphas)), np.nan)
	index = {(b, a): (i, j) for i, b in enumerate(betas) for j, a in enumerate(alphas)}
	for b, a, r, ar, pm in results:
		i, j = index[(b, a)]
		reward_grid[i, j] = r
		align_grid[i, j] = ar
		pos_grid[i, j] = pm

	def heatmap(grid: np.ndarray, title: str, out_path: str, vmin=None, vmax=None):
		plt.figure(figsize=(6, 4))
		plt.imshow(grid, aspect="auto", origin="lower", vmin=vmin, vmax=vmax, cmap="viridis")
		plt.colorbar()
		plt.xticks(range(len(alphas)), [str(a) for a in alphas])
		plt.yticks(range(len(betas)), [str(b) for b in betas])
		plt.xlabel("alpha (utility weight)")
		plt.ylabel("beta (coherence weight)")
		plt.title(title)
		plt.tight_layout()
		plt.savefig(out_path, dpi=150)
		plt.close()

	heatmap(reward_grid, "Mean reward (beta vs alpha)", "plots/ablation_reward_heatmap.png")
	heatmap(align_grid, "Alignment rate (action matches ctx)", "plots/ablation_alignment_heatmap.png", vmin=0.0, vmax=1.0)
	heatmap(pos_grid, "Position match (to target side)", "plots/ablation_posmatch_heatmap.png", vmin=0.0, vmax=1.0)

	print(f"Summary written: {csv_path}")
	print("Heatmaps: plots/ablation_reward_heatmap.png, plots/ablation_alignment_heatmap.png, plots/ablation_posmatch_heatmap.png")


if __name__ == "__main__":
	main()


