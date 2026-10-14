from volatility import mean, stdev
from returns import log_returns
from math import sqrt

def sharpe(prices, risk=0, ppy=252):

    fem_log = log_returns(prices)
    sigma = stdev(fem_log)

    if sigma <= 0:
        raise ValueError("Can not divide by 0!")

    per_period_ratio = (mean(fem_log) - risk) / sigma
    return per_period_ratio * sqrt(ppy)