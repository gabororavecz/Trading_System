def volatility_breakout(df, lookback=20, threshold=1.5):
    df['range'] = df['high'] - df['low']
    avg_range = df['range'].rolling(lookback).mean()
    latest_range = df['range'].iloc[-1]

    if latest_range > avg_range.iloc[-1] * threshold:
        return True
    return False

def market_regime(df):
    latest = df.iloc[-1]

    if latest['close'] > latest['ema20'] > latest['ema50']:
        return "STRONG UPTREND"

    if latest['close'] < latest['ema20'] < latest['ema50']:
        return "STRONG DOWNTREND"

    return "RANGE / CHOP"

def trade_score(df):
    def trade_score(df):

        score = 0

        # --- Trend (EMA) ---
        if df["close"].iloc[-1] > df["ema_200"].iloc[-1]:
            score += 1
        else:
            score -= 1

        # --- Momentum (RSI) ---
        rsi = df["rsi"].iloc[-1]

        if rsi < 30:
            score += 1  # oversold → bullish
        elif rsi > 70:
            score -= 1  # overbought → bearish

        # --- MACD ---
        if df["macd"].iloc[-1] > df["macd_signal"].iloc[-1]:
            score += 1
        else:
            score -= 1

        # --- Volume spike ---
        if df["volume"].iloc[-1] > df["volume"].rolling(20).mean().iloc[-1]:
            score += 1

        return score

def scan_market(df):
    latest = df.iloc[-1]

    signals = []

    if latest['rsi'] < 30:
        signals.append("OVERSOLD → Long candidate")

    if latest['rsi'] > 70:
        signals.append("OVERBOUGHT → Short candidate")

    if latest['close'] > latest['ema20'] > latest['ema50']:
        signals.append("Bullish momentum")

    if latest['close'] < latest['ema20'] < latest['ema50']:
        signals.append("Bearish momentum")

    if volatility_breakout(df):
        signals.append("Volatility breakout → Momentum trade")

    return signals







