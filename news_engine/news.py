import feedparser

def get_latest_news():

    feeds = [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss"
    ]

    news = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:  # limit per source
            news.append({
                "title": entry.title,
                "published_at": entry.get("published", ""),
                "source": feed.feed.get("title", "Unknown")
            })

    return news