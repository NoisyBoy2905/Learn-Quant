from volatility import mean

def sma(prices, window):
    if window < 1:
        raise ValueError("Window must be longer than 1 day!")
    if window > len(prices):
        return []
    total = []
    for i in range(len(prices) - window + 1):
        part = prices[i:i + window]
        total.append(mean(part))
    return total

def trend(prices, short=3, long=5):
    if len(prices) < long:
        raise ValueError("Prices needs to be longer than long window")

    s = sma(prices, short)[-1]
    l = sma(prices, long)[-1]

    gap = (s - l) / l
    if gap > 0.005: return "rising"
    if gap < -0.005: return "falling"
    return "flat"

assert sma([10, 11, 12, 13, 14, 15], 3) == [11, 12, 13, 14]
assert sma([10, 11], 3) == []
assert trend([10, 11, 12, 13, 14, 15, 16]) == "rising"     # short 15, long 14, gap +7.1%
assert trend([16, 15, 14, 13, 12, 11, 10]) == "falling"    # short 11, long 12, gap -8.3%
assert trend([10, 10.1, 9.9, 10, 10.1, 9.9, 10]) == "flat" # short 10, long 9.98, gap +0.2%