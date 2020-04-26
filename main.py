<<<<<<< Updated upstream
=======
import discord
import os

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


class SigameBotClient(discord.Client):
    def __init__(self):
        super().__init__()
        activity = discord.Activity(name='Свою Игру', type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)
        self.games = {}

    async def on_message(self, message):
        if message.author == self.user:
            return

        elif message.content.startswith('si! start'):
            if not message.startswith('si! start ') or len(message) <= 10:
                await message.channel.send("Чтобы начать игру, напишите 'si! start', затем имя пакета, с котроым вы хотите играть (через пробел)")
            pack_name = message.content[10:]
            if message.channel in self.games:
                await message.channel.send("Игра в этом канале уже началась")
            elif not pack_name:
                await message.channel.send("Необходимо передать имя пакета вопросов")
            else:
                try:
                    self.games[message.channel] = GameSession(pack_name)
                except ValueError:
                    await message.channel.send("данного пакета вопросов не существует")
                else:
                    await message.channel.send("Игра началась!")
                    await message.channel.send(f"Вы играете в \"{pack_name}\"\n" + 
                                                "Игроки могут присоединятся, написав 'si! join'")


class GameSession:
    def __init__(self, pack_name):
        self.pack_name = pack_name
        # здесь будет получение пака через API
        pass
        # ------
        self.members = {}

    def add_member(self, member):
        self.members[member] = 0


client = SigameBotClient()
client.run(TOKEN)

>>>>>>> Stashed changes
