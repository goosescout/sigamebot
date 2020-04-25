import discord
import os

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


class SigameBotClient(discord.Client):
    pass


client = SigameBotClient()
client.run(TOKEN)

