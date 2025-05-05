import os
from typing import Final
from datetime import date, timedelta

from newsapi import NewsApiClient
from dotenv import load_dotenv

# Load API key
load_dotenv()
NEWS_API_KEY: Final[str] = os.getenv('NEWS_API_KEY')

# Init client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

yesterday = date.today() - timedelta(days=1)
yesterday_str = yesterday.isoformat()  # Format: YYYY-MM-DD


def fetch_articles_by_language(lang_code):
    sources_data = newsapi.get_sources(language=lang_code)
    source_ids = [source['id'] for source in sources_data['sources']]
    sources_str = ','.join(source_ids)

    articles = newsapi.get_everything(
        q='tech',
        from_param=yesterday_str,
        to=yesterday_str,
        language=lang_code,
        sort_by='relevancy',
        sources=sources_str
    )
    return articles['articles']


def fetch_articles():
    all_articles = fetch_articles_by_language('fr') + fetch_articles_by_language('en')

    results = []
    for article in all_articles:
        results.append(f"- {article['title']} ({article['source']['name']})\n{article['url']}\n")

    return "\n".join(results)
