def generate_combined_signals(sentiment_signals, trading_data):

    combined = {}

    for coin, sentiment_data in sentiment_signals.items():

        sentiment = sentiment_data["signal"]

        trade_info = trading_data.get(coin, {})
        trade_score = trade_info.get("score", 0)
        regime = trade_info.get("regime", "")

        # --- Combine logic ---
        if sentiment == "BULLISH" and trade_score >= 2:
            final = "🔥 STRONG BUY"

        elif sentiment == "BEARISH" and trade_score <= -2:
            final = "🔥 STRONG SELL"

        # --- EARLY SIGNALS (important edge) ---
        elif sentiment == "NEUTRAL" and trade_score <= -2:
            final = "⚠️ EARLY BEARISH"

        elif sentiment == "NEUTRAL" and trade_score >= 2:
            final = "⚠️ EARLY BULLISH"

        else:
            final = "NO CLEAR EDGE"

        combined[coin] = {
            "sentiment": sentiment,
            "trade_score": trade_score,
            "regime": regime,
            "final_signal": final
        }

    return combined