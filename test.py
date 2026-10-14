import random
import time
from backtest import backtest, plot_backtest

price_generator = random.Random(42)
test_prices = [100.0]
for _ in range(299):
	test_prices.append(test_prices[-1] * (1 + price_generator.uniform(-0.05, 0.05)))

start_time = time.perf_counter()
results = backtest(test_prices, capital=1000.0, window=5)
end_time = time.perf_counter()

print(f"Time Taken: {end_time - start_time:.8f} seconds")
print("Portfolio History:", results)

plot_backtest(test_prices)