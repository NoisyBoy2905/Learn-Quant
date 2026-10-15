import random
import time; t_start = time.perf_counter()
import os
import csv
from backtest import backtest, plot_backtest
from sharpe_ratio import sharpe

starting_money = 1000

TICKERS = ["AAPL", "MSFT", "TSLA", "NVDA", "BTC-USD", "^FTSE", "KO", "JPM"]

def get_real_data(ticker, period="10y"):
	os.makedirs("data", exist_ok=True)
	filename = os.path.join("data", f"{ticker}_{period}.csv")

	if os.path.exists(filename):
		with open(filename) as f:
			reader = csv.reader(f)
			next(reader)
			return [float(row[1]) for row in reader]
	
	import yfinance as yf
	
	data = yf.download(ticker, period=period)
	close = data["Close"][ticker]
	fixed = close.dropna()
	fixed.to_csv(filename)
	
	return fixed.tolist()


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
		history, trades = backtest(prices)
		r = (history[-1] - start) / start
		returns.append(r)

		bh = (prices[-1] - prices[199]) / prices[199]
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
	print(f"Seeds with trades: {len(sharpes)}/{len(returns)}")
	print(f"Buy & Hold Average: {avg_bh:.1%} ")
	print(f"Stratergy beat buy and hold: {beat}/{len(returns)}")

def run_once(start):

	test_prices = get_real_data("NVDA")

	start_time = time.perf_counter()
	results, trades = backtest(test_prices, capital=1000.0)
	end_time = time.perf_counter()

	end = results[-1]
	ret = (end - start) / start

	print(f"Time Taken: {end_time - start_time:.8f} seconds")
	#print("Portfolio History:", results)
	print(f"Starting: £{start:.2f}")
	print(f"Final:    £{end:.2f}")
	print(f"Return:    {ret:.1%}")

	plot_backtest(test_prices, results)

def run_real_batch(start):

	returns = []
	sharpes = []
	bh_returns = []
	beat = 0

	for ticker in TICKERS:
		prices = get_real_data(ticker)
		history, trades = backtest(prices)
		r = (history[-1] - start) / start
		returns.append(r)

		bh = (prices[-1] - prices[199]) / prices[199]
		bh_returns.append(bh)

		n = len(trades)
		won = sum(1 for t in trades if t["profit"] > 0)
		if n > 0:
			avg_pct = sum(t["return_pct"] for t in trades) / n
		else:
			avg_pct = 0

		if r > bh:
			beat += 1 

		try:
			s = sharpe(history)
			sharpes.append(s)
		except ValueError:
			pass

		print(f"{ticker:8} statergy {r:6.1%}   Buy & Hold {bh:6.1%}")
		print(f"         trades {n}   won {won}   avg per trade {avg_pct:.1f}%")

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
	print(f"Seeds with trades: {len(sharpes)}/{len(returns)}")
	print(f"Buy & Hold Average: {avg_bh:.1%} ")
	print(f"Stratergy beat buy and hold: {beat}/{len(returns)}")

if __name__ == "__main__":


	print(f"Imports: {time.perf_counter() - t_start:.2f}s")
	run_real_batch(starting_money)