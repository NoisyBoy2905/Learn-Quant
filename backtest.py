from moving_averages import trend
from z_score import z_score

import matplotlib.pyplot as plt

def precom_indicators(prices, window):
    indicator = []

    for i in range(window, len(prices)):
        slice = prices[i - window: i + 1]
        t = trend(slice)
        z = z_score(slice)
        indicator.append({"index": i , "trend": t , "z_score": z})

    return indicator

def backtest(prices, capital=1000, window=5, fraction=0.2):

    indicator = precom_indicators(prices, window)
    cash = capital
    holding = 0 
    portfolio_history = []
    trades = []
    entry_price = 0.0

    for item in indicator:

        i = item["index"]
        current_price = prices[i]
        market_trend = item["trend"]
        z = item["z_score"]

        #print(f"Index: {i}, Price: {current_price}, Trend: {market_trend}, Z-Score: {z}")

        spend_cash = cash * fraction 

        if holding == 0:
            if market_trend in ["rising", "flat"] and z <= -1.5:
                holding = spend_cash / (current_price * 1.005)
                entry_price = current_price
                total_spent = spend_cash * 1.01 
                cash -= total_spent

        elif holding > 0:
            percent = (current_price - entry_price) / entry_price

            if percent >= 0.15 or percent <= -0.15 or (market_trend != "falling" and z >= 1.5):
                total_made = holding * (current_price * 0.995)
                cash += total_made
                profit = total_made - total_spent
                profit_percent = ((total_made / total_spent) - 1) * 100
                trades.append({"profit": profit, "return_pct": profit_percent})
                entry_price = 0.0
                holding = 0 

        portfolio_history.append(cash + (holding * current_price))

    return portfolio_history

def plot_backtest(prices, history):

    plt.subplot(2, 1, 1)
    plt.plot(prices, label="Price")
    plt.title("Prices")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(history, color="green", label="Portfolio")
    plt.axhline(1000, color="grey", linestyle="dotted", label="Start")
    plt.grid(True)
    plt.legend()
    plt.title("Backtest Curve")
    plt.xlabel("Day")
    plt.ylabel("Value")

    plt.tight_layout()
    plt.show()
