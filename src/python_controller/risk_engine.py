import pandas as pd
import numpy as np
from data_layer import build_candles
import MetaTrader5 as mt5

# Dynamic Risk Allocation
def dynamic_risk_allocation(equity=10000, base_risk=0.01, max_dd=0.08, volatility_multi=1.0, confidence=0.7):
    current_dd = 0.05  # Placeholder, calculate from history
    last_perf = 0.6  # Average win rate last 20 trades
    adjustment = min(1.5, max(0.5, (1 - current_dd / max_dd) * (last_perf / 0.55) * (1 / volatility_multi) * confidence))
    risk_pct = base_risk * adjustment
    print(f"Dynamic risk %: {risk_pct}")
    return risk_pct

# Portfolio Exposure Map
def portfolio_exposure_map(symbol="AUDCAD", equity=10000, position_size=0.1, max_exposure=0.06):
    # Placeholder for currency exposure
    usd_exposure = position_size / equity
    if usd_exposure > max_exposure:
        print("Exposure exceeded! Reject trade.")
        return False
    print("Exposure acceptable.")
    return True

# Equity Protection System
def equity_protection(current_dd=0.05, threshold=0.08):
    if current_dd >= threshold:
        print("Drawdown threshold reached! Entering Safe Mode.")
        return "Safe Mode"  # Stop trading for 24 hours
    print("Equity protected.")
    return "Normal"

# Correlation Engine
def correlation_engine(symbol1="AUDCAD", symbol2="EURUSD", count=50):
    df1 = build_candles(symbol1, count=count)['close']
    df2 = build_candles(symbol2, count=count)['close']
    corr = np.corrcoef(df1, df2)[0,1]
    if corr > 0.8:
        print("High correlation! Reject trade.")
        return False
    print("Correlation acceptable.")
    return True

if __name__ == "__main__":
    dynamic_risk_allocation()
    portfolio_exposure_map()
    equity_protection()
    correlation_engine()