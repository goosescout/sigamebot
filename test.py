import discord
import os
import json
import pymorphy2

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

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="SiGame"))

    async def start_game(self, channel):
        cur_game = self.games[channel]
        #morph = pymorphy2.MorphAnalyzer()
        #word = morph.parse('секунда')[0]
        cur_round = cur_game.update_round()
        categories = cur_game.get_categories()
        str_categories = '\n'.join(map(lambda x: '• ' + x[0] + ' - ' + x[1], categories.items()))
        await channel.send(f"Начинается {cur_round} раунд\n" +
                           f"Категории раунда:\n{str_categories}")
 

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
        except FileNotFoundError:
            await ctx.send("Пак не найден")
        else:
            await ctx.send("Начался сбор участников!")
            await ctx.send("Игроки могут присоединятся, написав 'si! join'\n" + 
                           "Чтобы завершить сбор игроков, напишите 'si! end'")

    @commands.command(name='join')
    async def join(self, ctx):
        if ctx.channel in self.bot.games.keys() and self.bot.games[ctx.channel].is_joinable():
            try:
                self.bot.games[ctx.channel].add_member(ctx.message.author)
            except Exception as ex:
                await ctx.send(ex)
            else:
                await ctx.send(f"К игре присоединяется {ctx.message.author.mention}!")

    @commands.command(name='end')
    async def end(self, ctx):
        if ctx.channel in self.bot.games.keys():
            cur_game = self.bot.games[ctx.channel]
            try:
                cur_game.end_join()
            except Exception as ex:
                await ctx.send(ex)
            else:
                await ctx.send("Сбор учатников закончен")
                await ctx.send("Игра началась!\n" +
                               f"Играется пак вопросов \"{cur_game.pack_name}\"\n" +
                               f"В игре {'участвуют' if len(cur_game.get_members()) > 1 else 'участвует'}: {', '.join(member.mention for member in cur_game.get_members(True))}")
                await self.bot.start_game(ctx.channel)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Такой команды не существует")


class GameSession:
    def __init__(self, pack_name):
        self.pack_name = pack_name
        # здесь будет получение пака через API
        
        with open(f'{pack_name}.json') as f:
            self.pack = json.load(f)

        # ------

        self.members = {}
        self.joinable = True

        self.cur_round = 0

    def add_member(self, member):
        if member in self.members.keys():
            raise ValueError(f"{member.mention}, ты уже в игре!")
        else:
            self.members[member] = 0

    def is_joinable(self):
        return self.joinable

    def get_members(self, names_only=False):
        return self.members.keys() if names_only else self.members

    def end_join(self):
        if self.joinable:
            if len(self.members) > 0:
                self.joinable = False
            else:
                raise ValueError('Нельзя начать игру, в которой нет игроков')

    def update_round(self):
        self.cur_round += 1
        return self.cur_round

    def get_categories(self):
        result = {}
        for category in self.pack['rounds'][self.cur_round - 1]['categories']:
            result[category['name']] = category['description']
        return result


bot = SiGameBot(command_prefix='si! ')
bot.add_cog(SiCommands(bot))
bot.run(TOKEN)
