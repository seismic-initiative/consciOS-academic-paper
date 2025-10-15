import os
import itertools
import subprocess


def run_cmd(cmd: str):
	print(f"→ {cmd}")
	subprocess.run(cmd, shell=True, check=True)


def main():
	os.makedirs("logs", exist_ok=True)
	betas = [0.0, 0.5, 1.0, 2.0]
	alphas = [0.0, 0.5, 1.0]
	for beta, alpha in itertools.product(betas, alphas):
		log = f"logs/hier_b{beta}_a{alpha}.csv"
		cmd = f"PYTHONPATH=code python -m agents.hier_agent --episodes 400 --seed 1 --beta {beta} --alpha {alpha} --freq_on true --egs_on true --log_path {log}"
		run_cmd(cmd)
		plot_reward = f"plots/hier_b{beta}_a{alpha}_reward.png"
		plot_pos = f"plots/hier_b{beta}_a{alpha}_pos.png"
		run_cmd(f"PYTHONPATH=code python -m plots.plot_traces_single --trace {log} --out_reward {plot_reward} --out_pos {plot_pos}")


if __name__ == "__main__":
	main()


