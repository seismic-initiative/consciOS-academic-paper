def resonance_score(expected_utility: float, coherence: float, cost: float, alpha: float, beta: float, gamma: float) -> float:
	return alpha * expected_utility + beta * coherence - gamma * cost


