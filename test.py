import discord
import os

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


class SiGameBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.games = {}

    async def on_message(self, message):
        await self.process_commands(message)


class SiCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='start')
    async def start(self, ctx, pack_name):
        if ctx.message.channel in self.bot.games.keys():
            await ctx.send("Игра в этом канале уже началась")
            return
        try:
            self.bot.games[ctx.message.channel] = GameSession(pack_name)
        except ValueError:
            pass
        else:
            await ctx.send(f"Начался сбор участников!")
            await ctx.send(f"Игроки могут присоединятся, написав 'si! join'\n" + 
                            "Чтобы завершить сбор игроков, напишите 'si! end'")

    @commands.command(name='join')
    async def join(self, ctx):
        if ctx.channel in self.bot.games.keys() and self.bot.games[ctx.channel].is_joinable():
            try:
                self.bot.games[ctx.channel].add_member(ctx.message.author)
            except ValueError as ex:
                await ctx.send(ex)
            else:
                await ctx.send(f"К игре присоединяется {ctx.message.author.mention}!")

    @commands.command(name='end')
    async def end(self, ctx):
        if ctx.channel in self.bot.games.keys():
            self.bot.games[ctx.channel].joinable = False
            await ctx.send("Сбор учатников закончен")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Такой команды не существует")


class GameSession:
    def __init__(self, pack_name):
        self.pack_name = pack_name
        # здесь будет получение пака через API
        pass
        # ------
        self.members = {}
        self.joinable = True

    def add_member(self, member):
        if member in self.members.keys():
            raise ValueError(f"{member.mention}, ты уже в игре!")
        else:
            self.members[member] = 0

    def is_joinable(self):
        return self.joinable


bot = SiGameBot(command_prefix='si! ')
bot.add_cog(SiCommands(bot))
bot.run(TOKEN)
