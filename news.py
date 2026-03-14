import feedparser


def get_news():

    url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US"

    feed = feedparser.parse(url)

    news = []

    for entry in feed.entries[:5]:

        title = entry.title
        link = entry.link

        news.append((title, link))

    return news


async def news(update, context):

    items = get_news()

    text = "📰 MARKET NEWS\n\n"

    for title, link in items:

        text += f"• {title}\n{link}\n\n"

    await update.message.reply_text(text)
