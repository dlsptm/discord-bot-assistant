from typing import Final, Optional
from discord import Message
from utils.news_api import fetch_articles
from utils.ollama import call_ollama
from utils.youtube import fetch_youtube_videos

DISCORD_MAX_MESSAGE_LENGTH: Final[int] = 2000  # Limite de 2000 caractères par message Discord

def get_response(user_input: str, channel: str) -> Optional[str]:
    lowered: str = user_input.strip().lower()

    if lowered.startswith("!ask ") or channel == 'chatbot':
        # Si la commande commence par "!ask ", on la retire
        lowered = lowered[5:] if lowered.startswith("!ask ") else lowered
        return call_ollama(lowered)
    elif lowered.startswith("!yt ") or channel == 'youtube':
        # Même logique pour les commandes YouTube
        lowered = lowered[4:] if lowered.startswith("!yt ") else lowered
        return fetch_youtube_videos(lowered)
    elif channel == 'news':
        return fetch_articles()
    elif lowered == "health check":
        return 'Hello there ! I am here'
    return None


def split_message(response: str)->list:
    messages = []
    while len(response) > DISCORD_MAX_MESSAGE_LENGTH:
        # Chercher la dernière occurrence de '\n' (saut de ligne) avant la limite
        split_index = response.rfind('\n', 0, DISCORD_MAX_MESSAGE_LENGTH)
        if split_index == -1:
            # Si aucun saut de ligne n'est trouvé, couper à la limite maximale
            split_index = DISCORD_MAX_MESSAGE_LENGTH

        # Diviser la réponse en une partie et continuer avec la suite
        part = response[:split_index]
        response = response[split_index:].lstrip()  # Retirer l'espace de début pour le prochain message
        messages.append(part)

    # Ajouter le reste du message (si ce n'était pas encore envoyé)
    if response:
        messages.append(response)

    return messages


async def send_message(message: Message, user_message: str, channel: str) -> None:
    if not user_message:
        return

    is_private: bool = user_message.startswith('?')
    user_message: str = user_message[1:] if is_private else user_message

    try:
        response: str = get_response(user_message, channel)

        if response is not None:
            messages = split_message(response)

            for part in messages:
                if is_private:
                    await message.author.send(part)
                else:
                    await message.channel.send(part)

    except Exception as e:
        print(f"Error occurred: {e}")
        await message.channel.send(f"An error occurred while processing your request. {e}")


