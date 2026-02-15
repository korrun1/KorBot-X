import pandas as pd
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from data_layer import build_candles
import MetaTrader5 as mt5

def mean_reversion(symbol="AUDCAD", count=50, bb_period=20, rsi_period=14, rsi_low=30, rsi_high=70):
    candles = build_candles(symbol, timeframe=mt5.TIMEFRAME_M5, count=count)
    if candles is None:
        return None
    df = candles[['open', 'high', 'low', 'close']].copy()
    bb = BollingerBands(close=df['close'], window=bb_period, window_dev=2)
    df.loc[:, 'BB_lower'] = bb.bollinger_lband()
    df.loc[:, 'BB_upper'] = bb.bollinger_hband()
    rsi = RSIIndicator(close=df['close'], window=rsi_period)
    df.loc[:, 'RSI'] = rsi.rsi()
    if df['close'].iloc[-1] < df['BB_lower'].iloc[-1] and df['RSI'].iloc[-1] < rsi_low:
        signal = "Buy"  # Oversold
    elif df['close'].iloc[-1] > df['BB_upper'].iloc[-1] and df['RSI'].iloc[-1] > rsi_high:
        signal = "Sell"  # Overbought
    else:
        signal = "Hold"
    print(f"Mean Reversion signal for {symbol}: {signal}")
    return signal

if __name__ == "__main__":
    mean_reversion()