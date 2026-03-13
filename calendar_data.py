import feedparser
import random


def get_calendar():

    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

    feed = feedparser.parse(url)

    events = []

    try:

        for entry in feed.entries[:6]:

            title = entry.title

            if hasattr(entry, "published"):
                date = entry.published
            else:
                date = "Upcoming"

            # impacto simulado

            impact = random.choice(["🔴", "🟠", "🟢"])

            events.append((impact, date, title))

    except:
        pass

    if len(events) == 0:

        events = [
            ("🔴", "Today", "US CPI Inflation"),
            ("🟠", "Tomorrow", "FED Rate Decision"),
            ("🟢", "This Week", "China Retail Sales")
        ]

    return events