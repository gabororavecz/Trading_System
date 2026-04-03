from datetime import datetime, timezone

def aggregate_sentiment(news, detect_coins, analyze_sentiment):

    scores = {}
    now = datetime.now(timezone.utc)

    for article in news:

        title = article.get("title", "")
        source = (article.get("source") or "").lower()

        coins = detect_coins(title)
        sentiment, score = analyze_sentiment(title)

        # --- Time weighting ---
        try:
            published_time = datetime.fromisoformat(
                article["published_at"].replace("Z", "+00:00")
            )
            minutes_ago = (now - published_time).total_seconds() / 60
            time_weight = max(0.1, 1 / (1 + minutes_ago / 60))
        except:
            time_weight = 0.5  # fallback if parsing fails

        # --- Source weighting ---
        if "reuters" in source or "bloomberg" in source:
            source_weight = 1.5
        elif "coindesk" in source or "cointelegraph" in source:
            source_weight = 1.2
        else:
            source_weight = 1.0

        # --- Combine weights ---
        final_weight = time_weight * source_weight

        for coin in coins:

            if coin not in scores:
                scores[coin] = []

            scores[coin].append(score * final_weight)

    # --- Aggregate results ---
    results = {}

    for coin, coin_scores in scores.items():

        if not coin_scores:
            continue

        avg_score = sum(coin_scores) / len(coin_scores)

        # --- Signal thresholds ---
        if avg_score > 0.15:
            signal = "BULLISH"
        elif avg_score < -0.15:
            signal = "BEARISH"
        else:
            signal = "NEUTRAL"

        results[coin] = {
            "articles": len(coin_scores),
            "average_sentiment": avg_score,
            "signal": signal
        }

    return results