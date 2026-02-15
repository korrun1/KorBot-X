import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import requests
import subprocess
import os

def connect_to_mt5():
    if not mt5.initialize():
        print("Failed to initialize MT5!")
        return False
    print("MT5 connected successfully!")
    return True

def get_tick_data(symbol="AUDCAD", count=100):
    if not connect_to_mt5():
        return None
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select symbol {symbol}!")
        mt5.shutdown()
        return None
    utc_from = datetime.utcnow() - timedelta(hours=24)  # Fetch ticks from last 24 hours
    utc_to = datetime.utcnow()
    ticks = mt5.copy_ticks_range(symbol, utc_from, utc_to, mt5.COPY_TICKS_ALL)
    mt5.shutdown()
    if ticks is None:
        error_code, error_msg = mt5.last_error()
        print(f"Failed to get tick data! Error: {error_code} - {error_msg}")
        return None
    if len(ticks) == 0:
        print("No ticks available in the specified range! Check if market is open or data is loaded in MT5.")
        return None
    return ticks

def build_candles(symbol="AUDCAD", timeframe=mt5.TIMEFRAME_M1, count=10):
    if not connect_to_mt5():
        return None
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select symbol {symbol}!")
        mt5.shutdown()
        return None
    utc_from = datetime.utcnow() - timedelta(minutes=count * 1)  # Adjust for M1 timeframe
    rates = mt5.copy_rates_from(symbol, timeframe, utc_from, count)
    mt5.shutdown()
    if rates is None or len(rates) == 0:
        print("Failed to build candles or no data available!")
        return None
    # Convert to DataFrame for easy handling
    df = pd.DataFrame(rates)
    df = df.assign(time=pd.to_datetime(df['time'], unit='s'))
    return df

def monitor_spread(symbol="AUDCAD", max_spread=2.0):
    if not connect_to_mt5():
        return None
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select symbol {symbol}!")
        mt5.shutdown()
        return None
    symbol_info = mt5.symbol_info(symbol)
    mt5.shutdown()
    if symbol_info is None:
        print("Failed to get symbol info!")
        return None
    current_spread = symbol_info.spread / 10.0  # Convert to pips
    print(f"Current spread for {symbol}: {current_spread} pips")
    if current_spread > max_spread:
        print("Spread too high! Avoid trading.")
        return False
    print("Spread acceptable.")
    return True

def track_slippage(symbol="AUDCAD", lot=0.01, max_slippage=1.0):
    if not connect_to_mt5():
        return None
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select symbol {symbol}!")
        mt5.shutdown()
        return None
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print("Failed to get tick info!")
        mt5.shutdown()
        return None
    price = tick.ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Slippage test",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_check(request)
    mt5.shutdown()
    if result is None or result.retcode != 0:
        error_code, error_msg = mt5.last_error()
        print(f"Failed to check order for slippage! Error: {error_code} - {error_msg}")
        return None
    slippage = abs(result.request.price - result.price) * 10  # In pips
    print(f"Slippage for {symbol}: {slippage} pips")
    if slippage > max_slippage:
        print("Slippage too high! Avoid trading.")
        return False
    print("Slippage acceptable.")
    return True

def filter_news_events(api_key="YOUR_ALPHA_VANTAGE_KEY", symbol="AUDCAD"):
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch news events!")
        return None
    data = response.json()
    if 'feed' in data and len(data['feed']) > 0:
        print("News events detected! Avoid trading during high impact news.")
        return False
    print("No significant news events.")
    return True

def process_with_rust(symbol="AUDCAD", count=50):
    df = build_candles(symbol, count=count)
    df.to_csv('raw_data.csv', index=False)
    subprocess.run(["cargo", "run"], cwd="../rust_core")
    # Use absolute path to processed_data.csv in rust_core
    processed_path = os.path.abspath('../rust_core/processed_data.csv')
    if not os.path.exists(processed_path):
        print("Processed file not found! Run 'cargo run' in rust_core first.")
        return None
    processed_df = pd.read_csv(processed_path)
    print("Processed data from Rust:", processed_df.head())
    return processed_df

if __name__ == "__main__":
    process_with_rust()