import MetaTrader5 as mt5
import time
import pandas as pd
import random
from data_layer import track_slippage, filter_news_events
from risk_engine import dynamic_risk_allocation, portfolio_exposure_map, equity_protection, correlation_engine

def execute_trade(signal, symbol="AUDCAD", lot=0.01, max_retries=3):
    if signal not in ["Buy", "Sell"]:
        print("No valid signal for execution.")
        return False
    if not mt5.initialize():
        print("Failed to initialize MT5 for execution!")
        return False

    # Safety checks
    if not track_slippage(symbol) or not filter_news_events(symbol=symbol) or not portfolio_exposure_map(symbol) or not correlation_engine() or equity_protection() == "Safe Mode":
        mt5.shutdown()
        return False

    # Dynamic lot
    risk_pct = dynamic_risk_allocation()
    lot = max(0.01, round(risk_pct * lot, 2))

    # Execution with retry and latency
    for attempt in range(max_retries):
        start_time = time.time()
        price = mt5.symbol_info_tick(symbol).ask if signal == "Buy" else mt5.symbol_info_tick(symbol).bid
        order_type = mt5.ORDER_TYPE_BUY if signal == "Buy" else mt5.ORDER_TYPE_SELL
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "price": price,
            "deviation": 10,
            "magic": 234000,
            "comment": "KorBot X Trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        latency = (time.time() - start_time) * 1000
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Trade executed: {signal} on {symbol} at {price}, lot {lot}, latency {latency:.2f} ms")
            mt5.shutdown()
            return True
        print(f"Attempt {attempt+1} failed, retcode {result.retcode}, retrying...")
        time.sleep(1)
    print("Execution failed after retries.")
    mt5.shutdown()
    return False

def self_diagnostics(trades=None):
    # Placeholder for real trades (list of dicts: {'profit': x, 'slippage': y})
    if trades is None:
        trades = [{'profit': random.uniform(-50, 100), 'slippage': random.uniform(0, 1)} for _ in range(20)]
    df = pd.DataFrame(trades)
    win_rate = (df['profit'] > 0).mean() * 100
    profit_factor = df[df['profit'] > 0]['profit'].sum() / abs(df[df['profit'] < 0]['profit'].sum()) if (df['profit'] < 0).any() else float('inf')
    avg_slippage = df['slippage'].mean()
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Profit Factor: {profit_factor:.2f}")
    print(f"Average Slippage: {avg_slippage:.2f} pips")
    if win_rate < 50:
        print("Performance declining - reducing risk.")
    else:
        print("Performance good.")

if __name__ == "__main__":
    execute_trade("Buy")
    self_diagnostics()