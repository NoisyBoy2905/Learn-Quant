from volatility import stdev, mean

def z_score(prices):

    sigma = stdev(prices)
    current_price = prices[-1]

    if sigma == 0:
        return 0 
    
    z = (current_price - mean(prices)) / sigma
    return z 
