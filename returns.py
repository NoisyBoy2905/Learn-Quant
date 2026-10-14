from math import log

def check_prices(prices):
    for price in prices:
        if price <= 0:
            raise ValueError("Not a real market value")

def simple_returns(prices):
    returns = []
    check_prices(prices)
    for i in range(1, len(prices)):
        r = (prices[i] - prices[i - 1]) / prices[i - 1]
        returns.append(r)
    return returns 

def log_returns(prices):
    returns = []
    check_prices(prices)
    for i in range(1, len(prices)):
        r = log(prices[i] / prices[i - 1])
        returns.append(r)
    return returns

"""
assert simple_returns([100, 110]) == [0.1]
assert round(log_returns([100, 110, 99])[0], 4) == 0.0953
assert round(sum(log_returns([100, 110, 99])), 4) == round(log(99 / 100), 4)
assert simple_returns([100]) == []
assert simple_returns([]) == []

try:
    print(simple_returns([100, 0, 50]))
    print("Failed: price of 0 was inputed")
except ValueError:
    pass

try:
    print(log_returns([100, 0, 50]))
    print("Failed: price of 0 was inputed")
except ValueError:
    pass
"""