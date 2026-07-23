import os
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import datetime

# loading important env variables
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# setting up
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

async def send_msg(msg: Message, user_msg: str):
    if not (user_msg):
        return

    private = user_msg[0] == "?"

    if private:
        user_msg = user_msg[1:]

    try:
        context = {
            "username": str(msg.author.id),
            "user_msg": msg.content,
            "guild": str(msg.guild.id)
        }
    except:
        context = {
               
                "username": str(msg.author.id),
                "user_msg": msg.content,
                "channel" : str(msg.channel.id)
                
        }
        
        print(context)
    try:
        response = get_response(context)

        if response is None:

            return

        await msg.author.send(response) if private else await msg.channel.send(response)

    except Exception as e:
        print(e)


# start the bot
@client.event
async def on_ready():
    print(f"{client.user} all systems go!")


# handle incoming messages
@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    await send_msg(msg, msg.content)


def main():
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
