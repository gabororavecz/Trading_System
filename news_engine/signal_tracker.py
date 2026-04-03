import json
import os

FILE_PATH = "last_signals.json"


def load_previous_signals():
    if not os.path.exists(FILE_PATH):
        return {}

    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_signals(signals):
    with open(FILE_PATH, "w") as f:
        json.dump(signals, f, indent=4)


def detect_changes(current_signals, previous_signals):

    alerts = []

    for coin, data in current_signals.items():

        current_signal = data["signal"]
        previous_signal = previous_signals.get(coin)

        if previous_signal is None:
            continue

        if current_signal != previous_signal:
            alerts.append(
                f"🚨 {coin} changed from {previous_signal} → {current_signal}"
            )

    return alerts