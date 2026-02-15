import pandas as pd
from ta.trend import EMAIndicator
from ta.volume import VolumeWeightedAveragePrice
from data_layer import build_candles
import MetaTrader5 as mt5

def smart_scalping(symbol="AUDCAD", count=50, ema_short=5, ema_long=13, vwap_period=14, confidence_threshold=0.7):
    candles = build_candles(symbol, timeframe=mt5.TIMEFRAME_M1, count=count)
    if candles is None:
        return None
    df = candles[['open', 'high', 'low', 'close', 'tick_volume']]
    ema_short_ind = EMAIndicator(close=df['close'], window=ema_short)
    ema_long_ind = EMAIndicator(close=df['close'], window=ema_long)
    df.loc[:, 'EMA_short'] = ema_short_ind.ema_indicator()
    df.loc[:, 'EMA_long'] = ema_long_ind.ema_indicator()
    vwap = VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'], volume=df['tick_volume'], window=vwap_period)
    df.loc[:, 'VWAP'] = vwap.volume_weighted_average_price()
    # Simple AI confidence simulation (replace with real AI later)
    confidence = 0.8  # Placeholder
    if df['EMA_short'].iloc[-1] > df['EMA_long'].iloc[-1] and df['close'].iloc[-1] > df['VWAP'].iloc[-1] and confidence > confidence_threshold:
        signal = "Buy"
    elif df['EMA_short'].iloc[-1] < df['EMA_long'].iloc[-1] and df['close'].iloc[-1] < df['VWAP'].iloc[-1] and confidence > confidence_threshold:
        signal = "Sell"
    else:
        signal = "Hold"
    print(f"Scalping signal for {symbol}: {signal}")
    return signal

if __name__ == "__main__":
    smart_scalping()