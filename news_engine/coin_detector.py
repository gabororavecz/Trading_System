from coins_config import TOP_COINS

def detect_coins(title):

    title = title.lower()
    detected = []

    for coin, keywords in TOP_COINS.items():

        for keyword in keywords:

            if keyword in title:
                detected.append(coin)
                break

    return detected