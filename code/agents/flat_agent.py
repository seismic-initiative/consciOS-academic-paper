import argparse
from env.shifty_grid import ShiftyGrid
from trace_logging.traces import TraceLogger


def run(episodes: int, seed: int, log_path: str = "logs/flat_traces.csv"):
	env = ShiftyGrid(seed=seed)
	logger = TraceLogger(path=log_path, header=[
		"episode","step","ctx","action","reward","norm_pos","score_left","score_right"
	])
	s = env.reset()
	ep, step = 0, 0
	while ep < episodes:
		# naive policy: always move toward right
		a = 1
		s, r, done, info = env.step(a)
		norm_pos = float(s[0])
		logger.log_row([ep, step, int(info.get("ctx", 0)), a, float(r), norm_pos, "", ""])  # scores empty for flat baseline
		step += 1
		if done:
			ep += 1
			step = 0
			s = env.reset()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--episodes", type=int, default=200)
	parser.add_argument("--seed", type=int, default=1)
	args = parser.parse_args()
	run(args.episodes, args.seed)


if __name__ == "__main__":
	main()


