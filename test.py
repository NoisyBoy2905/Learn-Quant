import random
import time
from backtest import backtest, plot_backtest


def make_prices(seed=None, fair_value=100.0, strength=0.05):
	gen = random.Random(seed)
	prices = [fair_value]
	for i in range(299):
		current = prices[-1]

		pull = strength * (fair_value - current)
		noise = gen.gauss(0, 0.02) * current
		next_price = current + pull + noise

		prices.append(next_price)

	return prices

returns = []

def run_batch():

	for seed in range(1, 101):
		prices = make_prices(seed)
		history = backtest(prices)
		r = (history[-1] - history[0]) / history[0]
		returns.append(r)

	average = sum(returns) / len(returns)
	wins = sum(1 for r in returns if r > 0)
	best = max(returns)
	worst = min(returns)

	print(f"Average return: {average:.1%}")
	print(f"Win rate: {wins}/{len(returns)}")
	print(f"Best: {best:.1%}")
	print(f"Worst: {worst:.1%}")

def run_once():

	test_prices = make_prices()

	start_time = time.perf_counter()
	results = backtest(test_prices, capital=1000.0, window=5)
	end_time = time.perf_counter()

	start = results[0]
	end = results[-1]
	ret = (end - start) / start

	print(f"Time Taken: {end_time - start_time:.8f} seconds")
	print("Portfolio History:", results)
	print(f"Starting: £{start:.2f}")
	print(f"Final:    £{end:.2f}")
	print(f"Return:    {ret:.1%}")

	plot_backtest(test_prices, results)

if __name__ == "__main__":

	run_once()
	run_batch()