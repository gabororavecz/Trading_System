from data import fetch_ohlcv
from indicators import add_indicators
from scanner import scan_market, market_regime, trade_score
from derivatives import get_funding_rate

symbols = [
    'BTC/USDT',
    'ETH/USDT',
    'SOL/USDT',
    'BNB/USDT',
    'XRP/USDT'
]

def run_scanner():

    results = {}

    for symbol in symbols:
        df = fetch_ohlcv(symbol)
        df = add_indicators(df)

        regime = market_regime(df)
        signals = scan_market(df)
        score = trade_score(df)

        symbol_futures = symbol.replace("/", "")
        funding = get_funding_rate(symbol_futures)

        coin = symbol.replace("/USDT", "")

        results[coin] = {
            "score": score,
            "regime": regime,
            "funding": funding
        }

    return results