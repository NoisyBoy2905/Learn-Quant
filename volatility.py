from returns import log_returns
import statistics
import math

def mean(values):
    return sum(values) / len(values)

def stdev(values):
    if len(values) < 2:
        raise ValueError("Need at least 2 values!")
    m = mean(values)
    total = 0
    for i in values:
        total = total + (i - m) ** 2
    variance = total / (len(values) - 1)
    return math.sqrt(variance)

def volatility(prices):
    return stdev(log_returns(prices))

"""
assert round(stdev([0.02, -0.01, 0.03, -0.02]), 4) == 0.0238, "jumpy item A wrong"
assert round(stdev([0.01, 0.0, 0.01, 0.0]), 4) == 0.0058, "steady item B wrong"
assert round(stdev([0.05, 0.05, 0.05])) == 0, "all-equal values should give 0"
assert round(stdev([3, 1, 4, 1, 5]), 6) == round(statistics.stdev([3, 1, 4, 1, 5]), 6), "doesn't match statistics.stdev"

try:
    stdev([0.01])
    print("FAIL: stdev allowed only 1 value")
except ValueError:
    pass

steady = [100, 101, 100, 101, 100]
jumpy = [100, 120, 90, 130, 85]
assert volatility(jumpy) > volatility(steady), "jumpy prices should be more volatile"

print(volatility(steady))
print(volatility(jumpy))
"""