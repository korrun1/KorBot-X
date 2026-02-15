import pandas as pd
from ta.volatility import AverageTrueRange
from ta.trend import ADXIndicator
from data_layer import build_candles
import MetaTrader5 as mt5
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def detect_market_regime(symbol="AUDCAD", count=50):
    candles = build_candles(symbol, timeframe=mt5.TIMEFRAME_M5, count=count)
    if candles is None:
        print("Failed to get candles for regime detection!")
        return None
    df = candles[['open', 'high', 'low', 'close', 'tick_volume']].copy()
    # Check for zero or invalid values to avoid division by zero
    if (df['high'] - df['low'] == 0).any():
        print("Warning: Zero range detected in candles, skipping regime detection.")
        return None
    atr = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14)
    df.loc[:, 'ATR_14'] = atr.average_true_range()
    adx = ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=14)
    df.loc[:, 'ADX_14'] = adx.adx()
    avg_atr = df['ATR_14'].mean()
    avg_adx = df['ADX_14'].mean()
    volatility_multiplier = df['ATR_14'].std() / avg_atr if avg_atr > 0 else 0
    if avg_adx > 25:
        regime = "TRENDING"
    else:
        regime = "RANGING"
    if volatility_multiplier > 1.5:
        volatility = "HIGH VOLATILITY"
    else:
        volatility = "LOW LIQUIDITY" if df['tick_volume'].mean() < 100 else "NORMAL"
    print(f"Market regime for {symbol}: {regime}, {volatility}")
    return {"regime": regime, "volatility": volatility}

if __name__ == "__main__":
    detect_market_regime()