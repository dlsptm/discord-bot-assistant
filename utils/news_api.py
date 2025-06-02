import os
from collections import defaultdict
from typing import Final
from datetime import date, timedelta, datetime
from newsapi.newsapi_client import NewsApiClient
from pytz import timezone
from dotenv import load_dotenv

# Load API key
load_dotenv()
NEWS_API_KEY: Final[str] = os.getenv('NEWS_API_KEY')

# Init client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

sent_articles = defaultdict(list)

def fetch_articles_by_language(lang_code):
    yesterday = date.today() - timedelta(days=1)
    yesterday_str = yesterday.isoformat()  # Format: YYYY-MM-DD

    articles = newsapi.get_everything(
        q='technology OR tech OR programming OR python OR javascript OR symfony OR php OR coding',
        from_param=yesterday_str,
        to=yesterday_str,
        language=lang_code,
        sort_by='relevancy',
    )
    return articles['articles']


def fetch_articles():
    all_articles = fetch_articles_by_language('fr') + fetch_articles_by_language('en')
    today = datetime.now(timezone('Europe/Paris'))
    today_str = today.strftime('%d-%m-%Y')
    two_days_ago = today - timedelta(days=2)
    two_days_ago_str = two_days_ago.strftime('%d-%m-%Y')

    if sent_articles[two_days_ago_str]:
        del sent_articles[two_days_ago_str]

    results = [f"# 📢 VOTRE NEWS DU JOUR {today_str}"]
    has_new_articles = False
    for article in all_articles:
        url = article['url']
        if articles_session(today_str, url):
            has_new_articles = True
            results.append(f"- **{article['title']}** ({article['source']['name']})\n{article['url']}\n")

    if not has_new_articles:
        results = ["Vous n'avez plus d'articles à ce jour."]

    return "\n".join(results)


def articles_session(today, url):
    if url in sent_articles[today]:
        return False  # Déjà envoyé
    sent_articles[today].append(url)
    return True