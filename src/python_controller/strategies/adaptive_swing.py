import pandas as pd
from ta.trend import EMAIndicator
from data_layer import build_candles
import MetaTrader5 as mt5

def adaptive_swing(symbol="AUDCAD", count=50, ema_short=50, ema_long=200):
    candles = build_candles(symbol, timeframe=mt5.TIMEFRAME_H4, count=count)
    if candles is None:
        return None
    df = candles[['open', 'high', 'low', 'close']]
    ema_short_ind = EMAIndicator(close=df['close'], window=ema_short)
    ema_long_ind = EMAIndicator(close=df['close'], window=ema_long)
    df.loc[:, 'EMA_short'] = ema_short_ind.ema_indicator()
    df.loc[:, 'EMA_long'] = ema_long_ind.ema_indicator()
    if df['EMA_short'].iloc[-1] > df['EMA_long'].iloc[-1] and df['close'].iloc[-1] > df['EMA_short'].iloc[-1]:
        signal = "Buy"
    elif df['EMA_short'].iloc[-1] < df['EMA_long'].iloc[-1] and df['close'].iloc[-1] < df['EMA_short'].iloc[-1]:
        signal = "Sell"
    else:
        signal = "Hold"
    print(f"Adaptive Swing signal for {symbol}: {signal}")
    return signal

if __name__ == "__main__":
    adaptive_swing()