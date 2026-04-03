from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):

    score = sia.polarity_scores(text)

    compound = score["compound"]

    if compound >= 0.3:
        sentiment = "POSITIVE"
    elif compound <= -0.3:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    return sentiment, compound