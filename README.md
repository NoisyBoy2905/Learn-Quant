# Learn Quant

Me learning quant maths by actually coding it, not just reading about it. Each file is a concept I worked through in Python, with my own tests to check it works.

## What's in here
- `returns.py` - simple and log returns
- `volatility.py` - mean, standard deviation and volatility
- `moving_averages.py` - moving averages and trend detection
- `z_score.py` - z-scores
- `sharpe_ratio.py` - Sharpe ratio
- `backtest.py` - a backtester for a buy-the-dip strategy, with a graph of the price and the portfolio
- `test.py` - makes fake market data and runs the backtester on it

## The backtester
The strategy buys when the price is a lot lower than normal (z-score below -1.5) and sells when it's back up (z-score above 1.5), or if it moves 15% either way.

To test it properly I made a price generator where prices get pulled back towards a fair value, then ran the strategy on 100 different random markets instead of just one. I tuned it on one set of 100 and checked it on a different 100 it had never seen, so I knew it wasn't just luck.

Results on both sets:
- about +2.9% average return
- won in 80-88 out of 100 markets
- beat just buying and holding in 67-68 out of 100
- Sharpe ratio of about 0.6

Things I learned along the way: the strategy lost money on pure random data (there's no pattern to find, so fees eat you), a 5 day window was too short to tell what "cheap" means, and selling early made the win rate slightly better but the return worse.

All written by me while learning. I'll keep adding to it as I go.