import os
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import tasks, commands
from utils import news_api
from utils.functions import split_message, send_message

load_dotenv()

DISCORD_TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
GOOGLE_TOKEN: Final[str] = os.getenv('GOOGLE_TOKEN')
NEWS_CHANNEL_ID: Final[int] = int(os.getenv('NEWS_CHANNEL_ID'))

intents : Intents = Intents.default()
intents.message_content: bool = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f'✅ {client.user} is now running.')
    if not send_daily_news.is_running():
        send_daily_news.start()


@tasks.loop(hours=24)
async def send_daily_news():
    channel = client.get_channel(NEWS_CHANNEL_ID)
    if channel:
        news_response = news_api.fetch_articles()
        messages = split_message(news_response)
        for msg in messages:
            await channel.send(msg)
    else:
        print("❌ Channel not found.")


@send_daily_news.before_loop
async def before():
    print('waiting...')
    await client.wait_until_ready()


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    user_message: str = message.content
    channel : str = str(message.channel)

    await  send_message(message, user_message, channel)


def main():
    if not DISCORD_TOKEN or not GOOGLE_TOKEN:
        raise ValueError("DISCORD_TOKEN or GOOGLE_TOKEN not found in environment variables.")
    client.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()