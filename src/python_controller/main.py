import data_layer
import market_intel
import strategy_engine
import ai_optimization
import risk_engine
import execution_engine
from backtesting.backtester import backtest_strategy, monte_carlo_simulation, walk_forward_test
import pandas as pd
from datetime import datetime
from databases import init_sqlite, save_trade_sqlite, save_real_time_data, get_real_time_data
from telegram_notify import send_telegram_notification
import time

def run_bot():
    init_sqlite()
    while True:
        data_layer.connect_to_mt5()
        ticks = data_layer.get_tick_data()
        if ticks is not None:
            print("Tick data retrieved successfully!")
        candles = data_layer.build_candles()
        if candles is not None:
            print("Candle data built successfully!")
        spread_ok = data_layer.monitor_spread()
        if spread_ok is not None:
            print("Spread monitoring completed!")
        slippage_ok = data_layer.track_slippage()
        if slippage_ok is not None:
            print("Slippage tracking completed!")
        news_ok = data_layer.filter_news_events()
        if news_ok is not None:
            print("News filter completed!")
        regime = market_intel.detect_market_regime()
        if regime is not None:
            print("Market regime detection completed!")
            save_real_time_data("current_regime", regime)
            print("Retrieved regime from Redis:", get_real_time_data("current_regime"))
        signal = strategy_engine.run_strategy_engine()
        if signal is not None:
            print("Strategy Engine completed!")
        # Test AI layer
        df = data_layer.build_candles(count=50)
        ai_optimization.confidence_scoring(df)
        ai_optimization.optimize_exit(df)
        ai_optimization.auto_optimize_params()
        print("AI Optimization completed!")
        # Test Risk Engine
        risk_engine.dynamic_risk_allocation()
        risk_engine.portfolio_exposure_map()
        risk_engine.equity_protection()
        risk_engine.correlation_engine()
        print("Risk Engine completed!")
        # Execution
        execution_engine.execute_trade(signal)
        # Save trade example
        save_trade_sqlite("AUDCAD", signal, 1.05, str(datetime.now()), 50.0)
        # Notification
        send_telegram_notification("YOUR_TOKEN", "YOUR_CHAT_ID", f"Signal: {signal}")
        # Monitoring
        execution_engine.self_diagnostics()
        # Backtesting (periodic)
        returns = pd.Series([0.001] * 252)  # Placeholder
        backtest_strategy()
        monte_carlo_simulation(returns)
        walk_forward_test()
        print("Cycle completed! Sleeping for 60 seconds...")
        time.sleep(60)  # Run every minute

if __name__ == "__main__":
    # Run GUI with bot
    from gui.dashboard import KorBotDashboard
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = KorBotDashboard()
    window.show()
    sys.exit(app.exec())