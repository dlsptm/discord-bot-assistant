import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from utils import news_api
from utils.functions import *
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

load_dotenv()


DISCORD_TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
GOOGLE_TOKEN: Final[str] = os.getenv('GOOGLE_TOKEN')
NEWS_CHANNEL_ID: Final[int] = int(os.getenv('NEWS_CHANNEL_ID'))

intents : Intents = Intents.default()
intents.message_content: bool = True
client : Client = Client(intents=intents)

paris = timezone('Europe/Paris')
scheduler = AsyncIOScheduler(timezone=paris)


@scheduler.scheduled_job(CronTrigger(hour=9, minute=30, timezone=paris))
async def send_daily_news():
    today = datetime.today()
    channel_id = NEWS_CHANNEL_ID
    channel = client.get_channel(channel_id)
    if channel:
        news_response = news_api.fetch_articles()
        messages = [f"# 📢 VOTRE NEWS DU JOUR {today.strftime('%d-%m-%Y')}"] + split_message(news_response)
        for msg in messages:
            await channel.send(msg)


@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')
    scheduler.start()


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    user_message: str = message.content
    channel : str = str(message.channel)

    await  send_message(message, user_message, channel)


def main():
    client.run(token=DISCORD_TOKEN)


if __name__ == '__main__':
    if not DISCORD_TOKEN or not GOOGLE_TOKEN:
        raise ValueError("DISCORD_TOKEN or GOOGLE_TOKEN not found in environment variables.")
    main()