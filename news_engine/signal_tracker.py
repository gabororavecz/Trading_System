import json
import os

FILE_PATH = "last_signals.json"


def load_previous_signals():
    """Load the last saved signals from JSON file, handling old formats."""
    if not os.path.exists(FILE_PATH):
        return {}

    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # Malformed JSON, ignore and start fresh
        return {}

    # Ensure the structure is {coin: {"signal": ..., "avg_sentiment": ...}}
    cleaned = {}
    for coin, value in data.items():
        if isinstance(value, dict):
            # Already in new format
            cleaned[coin] = {"signal": value.get("signal"), "avg_sentiment": value.get("avg_sentiment", 0)}
        else:
            # Old format: value is just the signal string
            cleaned[coin] = {"signal": value, "avg_sentiment": 0}

    return cleaned


def save_signals(signals):
    """Save current signals to JSON file in standardized format."""
    to_save = {}
    for coin, data in signals.items():
        if isinstance(data, dict):
            to_save[coin] = {"signal": data.get("signal"), "avg_sentiment": data.get("avg_sentiment", 0)}
        else:
            # fallback: if data is a string
            to_save[coin] = {"signal": data, "avg_sentiment": 0}

    with open(FILE_PATH, "w") as f:
        json.dump(to_save, f, indent=4)


def detect_signal_changes(current_signals):
    """
    Compare current signals to the previous ones and return a list of alerts.

    current_signals should be a dict:
    {
        "BTC": {"signal": "BULLISH", "avg_sentiment": 0.2},
        "ETH": {"signal": "BEARISH", "avg_sentiment": -0.1},
        ...
    }
    """
    previous_signals = load_previous_signals()
    alerts = []

    for coin, data in current_signals.items():
        # Current signal
        current_signal = data.get("signal") if isinstance(data, dict) else data

        # Previous signal
        prev_data = previous_signals.get(coin)
        previous_signal = prev_data.get("signal") if isinstance(prev_data, dict) else prev_data

        if previous_signal is None:
            # First time seeing this coin, no alert
            continue

        if current_signal != previous_signal:
            alerts.append(f"🚨 {coin} changed from {previous_signal} → {current_signal}")

    # Save the new signals for the next run
    save_signals(current_signals)
    return alerts