import pandas as pd
from ta.trend import EMAIndicator
from data_layer import build_candles
import MetaTrader5 as mt5

def breakout(symbol="AUDCAD", count=50, short_period=5, long_period=14, breakout_threshold=1.5):
    candles = build_candles(symbol, timeframe=mt5.TIMEFRAME_H1, count=count)
    if candles is None:
        return None
    df = candles[['open', 'high', 'low', 'close', 'tick_volume']]
    session_high = df['high'].max()
    session_low = df['low'].min()
    ema_short_vol = EMAIndicator(close=df['tick_volume'], window=short_period)
    ema_long_vol = EMAIndicator(close=df['tick_volume'], window=long_period)
    df.loc[:, 'EMA_short_vol'] = ema_short_vol.ema_indicator()
    df.loc[:, 'EMA_long_vol'] = ema_long_vol.ema_indicator()
    df.loc[:, 'Volume_Osc'] = ((df['EMA_short_vol'] - df['EMA_long_vol']) / df['EMA_short_vol']) * 100
    if df['close'].iloc[-1] > session_high and df['Volume_Osc'].iloc[-1] > breakout_threshold:
        signal = "Buy"
    elif df['close'].iloc[-1] < session_low and df['Volume_Osc'].iloc[-1] > breakout_threshold:
        signal = "Sell"
    else:
        signal = "Hold"
    print(f"Breakout signal for {symbol}: {signal}")
    return signal

if __name__ == "__main__":
    breakout()