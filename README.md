# Learn Quant

Me learning quant maths by actually coding it, not just reading about it. Each file is a concept I worked through in Python, with my own tests to check it works.

## What's in here
- `returns.py` - simple and log returns
- `volatility.py` - mean, standard deviation and volatility
- `moving_averages.py` - moving averages and trend detection
- `z_score.py` - z-scores
- `sharpe_ratio.py` - Sharpe ratio
- `backtest.py` - a backtester for a buy-the-dip strategy, with a graph of the price and the portfolio
- `test.py` - runs the backtester on fake market data and on real prices

## The backtester
The strategy buys when the price is a lot lower than normal (z-score below -1.5) and sells when it's back up (z-score above 1.5), or if it moves 15% either way.

### On fake data
I made a price generator where prices get pulled back towards a fair value, then ran the strategy on 100 different random markets instead of just one. I tuned it on one set of 100 and checked it on a different 100 it had never seen, so I knew it wasn't just luck.

- about +2.9% average return
- won in 80-88 out of 100 markets
- beat just buying and holding in 67-68 out of 100
- Sharpe ratio of about 0.6

### On real data
Then I pulled real prices with yfinance for 8 markets (Apple, Microsoft, Tesla, Nvidia, Bitcoin, the FTSE 100, Coca-Cola and JP Morgan) and tested over 2 years and 10 years.

It made money on 6 out of 8, but lost to just buying and holding on all 8. Over 10 years buy and hold was massively ahead, for example Nvidia did +9,559% while my strategy did +39%.

Why it lost:
- Real stocks mostly trended up instead of bouncing back to a fair value, so waiting for dips meant sitting in cash while they climbed
- It only puts 20% of the money in at a time
- On Bitcoin it kept buying dips that kept falling (-37%)

Also worth saying: I picked these markets knowing they did well, so buy and hold looks better than it would have if I'd picked them 10 years ago (survivorship bias).

### Trend filter
To fix the trending problem I added a 200 day average so it only buys dips when the long term trend is up.

It made things worse. The average return dropped from 6.6% to 1.4% over 10 years and it still lost to buy and hold on all 8. The trend filter stops it buying bad dips, but that wasn't the real problem. The real problem is that it's hardly ever invested, and the filter just made it sit in cash even more. Bitcoin still lost 34.6%, so something else is losing money on each trade, which I want to look into next.

## Things I learned
- The strategy lost money on pure random data (there's no pattern to find, so fees eat you)
- A 5 day window was too short to tell what "cheap" means, 30 worked much better
- Selling early made the win rate slightly better but the return worse
- A strategy that works on fake data can completely fail on real data, so you have to test on both
- Downloading data every run was the slowest part, so I cached it and moved heavy imports so they only load when needed (8 seconds down to 0.1)

All written by me while learning. I'll keep adding to it as I go.