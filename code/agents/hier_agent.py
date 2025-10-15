import argparse
import numpy as np
from env.shifty_grid import ShiftyGrid
from selection.resonance import resonance_score
from trace_logging.traces import TraceLogger


def run(episodes: int, seed: int, beta: float, alpha: float, freq_on: bool, egs_on: bool, log_path: str = "logs/hier_traces.csv"):
	env = ShiftyGrid(seed=seed)
	logger = TraceLogger(path=log_path, header=[
		"episode","step","ctx","action","reward","norm_pos","score_left","score_right"
	])
	s = env.reset()
	ep, step = 0, 0
	while ep < episodes:
		# placeholder coherence/util estimates
		eu_left, eu_right = 0.1, 0.1
		# coherence shaped by context (ctx>0 favors right), with small noise
		base, delta = 0.6, 0.2
		ctx = int(s[1] * 2 - 1)  # reconstruct ctx in {-1, +1} from normalized signal
		c_right = base + (delta if ctx > 0 else -delta) + float(np.random.normal(0.0, 0.05))
		c_left = base - (delta if ctx > 0 else -delta) + float(np.random.normal(0.0, 0.05))
		c_right = float(max(0.0, min(1.0, c_right)))
		c_left = float(max(0.0, min(1.0, c_left)))
		cost_left, cost_right = 0.05, 0.05
		score_left = resonance_score(eu_left, c_left, cost_left, alpha, beta, 0.0)
		score_right = resonance_score(eu_right, c_right, cost_right, alpha, beta, 0.0)
		a = 1 if score_right >= score_left else -1
		s, r, done, info = env.step(a)
		norm_pos = float(s[0])
		logger.log_row([ep, step, int(info.get("ctx", 0)), a, float(r), norm_pos, score_left, score_right])
		step += 1
		if done:
			ep += 1
			step = 0
			s = env.reset()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--episodes", type=int, default=200)
	parser.add_argument("--seed", type=int, default=1)
	parser.add_argument("--beta", type=float, default=1.0)
	parser.add_argument("--alpha", type=float, default=0.5)
	parser.add_argument("--freq_on", type=str, default="true")
	parser.add_argument("--egs_on", type=str, default="true")
	parser.add_argument("--log_path", type=str, default="logs/hier_traces.csv")
	args = parser.parse_args()
	run(args.episodes, args.seed, args.beta, args.alpha, args.freq_on.lower()=="true", args.egs_on.lower()=="true", args.log_path)


