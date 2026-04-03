from price_reaction import get_price_window, volatility_reaction

def analyze_event_impact(news):
    reactions = []

    for item in news:
        for coin in item["currencies"]:
            symbol = f"{coin}/USDT"

            try:
                df = get_price_window(symbol)
                vol = volatility_reaction(df)

                reactions.append({
                    "asset": symbol,
                    "headline": item["title"],
                    "volatility": vol
                })
            except:
                pass

    return reactions