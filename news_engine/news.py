import feedparser
from datetime import datetime

RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://cryptoslate.com/feed/",
    "https://bitcoinmagazine.com/.rss/full/",
]

def parse_date(entry):
    try:
        return entry.get("published", "")
    except:
        return ""

def get_latest_news():
    news = []
    seen_titles = set()

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.get("title", "")

            # Deduplicate articles
            if title in seen_titles:
                continue
            seen_titles.add(title)

            news.append({
                "title": title,
                "published_at": parse_date(entry),
                "link": entry.get("link"),
                "source": feed.feed.get("title", "Unknown"),
                "currencies": []  # detected later
            })

    return news