from binance.client import Client

client = Client()

def get_funding_rate(symbol="BTCUSDT"):
    data = client.futures_funding_rate(symbol=symbol, limit=1)
    return float(data[0]["fundingRate"])

def funding_signal(funding):
    if funding > 0.0008:
        return "Crowded LONG → Short bias"
    elif funding < -0.0008:
        return "Crowded SHORT → Long bias"
    return "Neutral positioning"
