import ccxt
import pandas as pd

exchange = ccxt.binance()

def fetch_ohlcv(symbol='BTC/USDT', timeframe='5m', limit=200):
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(
        bars, columns=['timestamp','open','high','low','close','volume']
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
