import random
import time
from backtest import backtest, plot_backtest
from sharpe_ratio import sharpe

starting_money = 1000

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

def run_batch(start):

	returns = []
	sharpes = []
	bh_returns = []
	beat = 0

	for seed in range(101, 201):
		prices = make_prices(seed)
		history = backtest(prices)
		r = (history[-1] - start) / start
		returns.append(r)

		bh = (prices[-1] - prices[30]) / prices[30]
		bh_returns.append(bh)

		if r > bh:
			beat += 1 

		try:
			s = sharpe(history)
			sharpes.append(s)
		except ValueError:
			pass

	average = sum(returns) / len(returns)
	wins = sum(1 for r in returns if r > 0)
	best = max(returns)
	worst = min(returns)
	avg_sharpe = sum(sharpes) / len(sharpes)
	avg_bh = sum(bh_returns) / len(bh_returns)

	print(f"Average return: {average:.1%}")
	print(f"Win rate: {wins}/{len(returns)}")
	print(f"Best: {best:.1%}")
	print(f"Worst: {worst:.1%}")
	print(f"Average Sharpe: {avg_sharpe:.2f}")
	print(f"Seeds with trades: {len(sharpes)}/100")
	print(f"Buy & Hold Average: {avg_bh:.1%} ")
	print(f"Stratergy beat buy and hold: {beat}/100")

def run_once(start):

	test_prices = make_prices()

	start_time = time.perf_counter()
	results = backtest(test_prices, capital=1000.0)
	end_time = time.perf_counter()

	end = results[-1]
	ret = (end - start) / start

	print(f"Time Taken: {end_time - start_time:.8f} seconds")
	print("Portfolio History:", results)
	print(f"Starting: £{start:.2f}")
	print(f"Final:    £{end:.2f}")
	print(f"Return:    {ret:.1%}")

	plot_backtest(test_prices, results)

if __name__ == "__main__":

	run_batch(starting_money)