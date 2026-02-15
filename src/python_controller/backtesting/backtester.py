import pandas as pd
import numpy as np
from data_layer import build_candles
from strategy_engine import run_strategy_engine
import MetaTrader5 as mt5
from ai_optimization import auto_optimize_params

def backtest_strategy(symbol="AUDCAD", timeframe=mt5.TIMEFRAME_H1, count=1000):
    candles = build_candles(symbol, timeframe, count)
    if candles is None:
        return None
    df = candles.copy()
    signals = []
    for i in range(14, len(df)):  # Skip initial for indicators
        # Simulate signal for each bar (placeholder, integrate real engine)
        signal = run_strategy_engine(symbol)  # Use real engine for signals
        signals.append(signal)
    df = df.iloc[14:]
    df['signal'] = signals
    df['return'] = df['close'].pct_change()
    df['strategy_return'] = np.where(df['signal'] == "Buy", df['return'], np.where(df['signal'] == "Sell", -df['return'], 0))
    equity = (1 + df['strategy_return']).cumprod()
    win_rate = (df['strategy_return'] > 0).mean() * 100
    profit_factor = df[df['strategy_return'] > 0]['strategy_return'].sum() / abs(df[df['strategy_return'] < 0]['strategy_return'].sum()) if (df['strategy_return'] < 0).any() else np.inf
    mean_ret = df['strategy_return'].mean()
    std_ret = df['strategy_return'].std()
    sharpe = mean_ret / std_ret * np.sqrt(252) if std_ret > 0 else 0  # Annualized, avoid division by zero
    max_dd = (equity / np.maximum.accumulate(equity) - 1).min() * 100
    print(f"Backtest Results: Win Rate {win_rate:.2f}%, Profit Factor {profit_factor:.2f}, Sharpe {sharpe:.2f}, Max DD {max_dd:.2f}%")
    return {"win_rate": win_rate, "profit_factor": profit_factor, "sharpe": sharpe, "max_dd": max_dd}

def monte_carlo_simulation(returns, num_sim=1000, num_days=252):
    avg_return = returns.mean()
    std_return = returns.std()
    sims = np.random.normal(avg_return, std_return, (num_sim, num_days))
    equity_sims = (1 + sims).cumprod(axis=1)
    max_dd_sims = (equity_sims / np.maximum.accumulate(equity_sims, axis=1) - 1).min(axis=1)
    print(f"Monte Carlo Max DD 95% CI: {np.percentile(max_dd_sims, 95):.2f}%")
    return np.percentile(max_dd_sims, 95)

def walk_forward_test(symbol="AUDCAD", in_sample=500, out_sample=250):
    candles = build_candles(symbol, count=in_sample + out_sample)
    in_df = candles.iloc[:in_sample]
    out_df = candles.iloc[in_sample:]
    # Optimize on in-sample
    best_params = auto_optimize_params()
    # Test on out-sample (placeholder)
    results = backtest_strategy(symbol, count=out_sample)
    print(f"Walk Forward Results: {results}")
    return results

if __name__ == "__main__":
    backtest_strategy()
    monte_carlo_simulation(pd.Series([0.001] * 252))
    walk_forward_test()