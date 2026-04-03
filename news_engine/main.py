from news_engine.news import get_latest_news
from news_engine.event_analyzer import analyze_event_impact
from coin_detector import detect_coins
from news_engine.sentiment_analyzer import analyze_sentiment
from news_engine.sentiment_aggregator import aggregate_sentiment
from signal_tracker import load_previous_signals, save_signals, detect_changes
from news_engine.telegram_alert import send_telegram_message
from news_engine.signal_tracker import detect_signal_changes
from news_engine.combined_signals import generate_combined_signals
from crypto_scanner.scanner_runner import run_scanner
from crypto_scanner.scanner_runner import run_scanner

news = get_latest_news()
reactions = analyze_event_impact(news)

if not news:
    print("No news returned.")
else:
    for article in news[:5]:

        coins = detect_coins(article["title"])
        sentiment, score = analyze_sentiment(article["title"])

        print("-" * 50)
        print("Title:", article["title"])
        print("Published:", article["published_at"])
        print("Detected coins:", coins)
        print("Sentiment:", sentiment)
        print("Score:", score)


for r in sorted(reactions, key=lambda x: x["volatility"], reverse=True)[:5]:
    print("\nASSET:", r["asset"])
    print("VOLATILITY REACTION:", round(r["volatility"], 3), "%")
    print("HEADLINE:", r["headline"])

import nltk
nltk.download('vader_lexicon')

signals = aggregate_sentiment(news, detect_coins, analyze_sentiment)

print("\n===== MARKET SENTIMENT =====")

for coin, data in signals.items():

    print(f"\n{coin}")
    print("Articles:", data["articles"])
    print("Average Sentiment:", round(data["average_sentiment"], 3))
    print("Signal:", data["signal"])

previous = load_previous_signals()

alerts = detect_changes(signals, previous)

print("\n===== ALERTS =====")

if alerts:
    for alert in alerts:
        print(alert)
        send_telegram_message(alert)
else:
    print("No signal changes.")

# Save current signals for next run
simple_signals = {coin: data["signal"] for coin, data in signals.items()}
save_signals(simple_signals)

trading_data = run_scanner()

print("\nTRADING DATA:")
print(trading_data)

combined = generate_combined_signals(signals, trading_data)

print("\n===== FINAL SIGNALS =====")

for coin, data in combined.items():

    print(f"\n{coin}")
    print("Sentiment:", data["sentiment"])
    print("Trade Score:", data["trade_score"])
    print("Regime:", data["regime"])
    print("FINAL SIGNAL:", data["final_signal"])