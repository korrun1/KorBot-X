from market_intel import detect_market_regime
from strategies.scalping import smart_scalping
from strategies.mean_reversion import mean_reversion
from strategies.breakout import breakout
from strategies.adaptive_swing import adaptive_swing
from ai_optimization import confidence_scoring
from data_layer import build_candles

def run_strategy_engine(symbol="AUDCAD"):
    regime = detect_market_regime(symbol)
    if regime is None:
        return None
    if regime['regime'] == "TRENDING":
        signal = breakout(symbol)
    elif regime['volatility'] == "HIGH VOLATILITY":
        signal = smart_scalping(symbol)
    elif regime['regime'] == "RANGING":
        signal = mean_reversion(symbol)
    elif regime['volatility'] == "LOW LIQUIDITY":
        signal = adaptive_swing(symbol)
    else:
        signal = "Hold"
    # Integrate AI confidence
    candles = build_candles(symbol, count=50)
    confidence = confidence_scoring(candles)
    if confidence < 0.6:
        signal = "Hold (Low Confidence)"
    print(f"Final signal from Strategy Engine: {signal} with confidence {confidence}")
    return signal

if __name__ == "__main__":
    run_strategy_engine()