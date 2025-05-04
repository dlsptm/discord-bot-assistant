from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()


DISCORD_TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
GOOGLE_TOKEN: Final[str] = os.getenv('GOOGLE_TOKEN')
DISCORD_MAX_MESSAGE_LENGTH: Final[int] = 2000  # Limite de 2000 caractères par message Discord

intents : Intents = Intents.default()
intents.message_content: bool = True
client : Client = Client(intents=intents)

async def send_message(message: Message, user_message: str, channel: str) -> None:
    if not user_message:
        return

    is_private: bool = user_message.startswith('?')
    user_message: str = user_message[1:] if is_private else user_message

    try:
        response: str = get_response(user_message, channel)

        # Diviser la réponse en plusieurs messages si elle est trop longue
        while len(response) > DISCORD_MAX_MESSAGE_LENGTH:
            # Chercher la dernière occurrence de '\n' (saut de ligne) avant la limite
            split_index = response.rfind('\n', 0, DISCORD_MAX_MESSAGE_LENGTH)
            if split_index == -1:
                # Si aucun saut de ligne n'est trouvé, couper à la limite maximale
                split_index = DISCORD_MAX_MESSAGE_LENGTH

            # Diviser la réponse en une partie et continuer avec la suite
            part = response[:split_index]
            response = response[split_index:].lstrip()  # Retirer l'espace de début pour le prochain message

            if is_private:
                await message.author.send(part)
            else:
                await message.channel.send(part)

        # Envoi du reste du message (si ce n'était pas encore envoyé)
        if response:
            if is_private:
                await message.author.send(response)
            else:
                await message.channel.send(response)

    except Exception as e:
        print(f"Error occurred: {e}")
        await message.channel.send(f"An error occurred while processing your request. {e}")


@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')


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