import discord
import os
import json
import pymorphy2
import random

from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont


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
                           f"Категории раунда:\n{str_categories}", file=discord.File(cur_game.get_image_path()))
        await channel.send(f"Игру начинает {cur_game.get_cur_player().mention}\n" +
                           "Вам необходимо выбрать категорию. Для этого введите: 'название категории' 'номинал вопроса' (регистр не учитывается)")
 

class SiCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='start')
    async def start(self, ctx, pack_name):
        if ctx.message.channel in self.bot.games.keys():
            await ctx.send("Игра в этом канале уже началась")
            return
        try:
            self.bot.games[ctx.message.channel] = GameSession(pack_name, ctx.message.channel.id)
        except FileNotFoundError:
            await ctx.send("Пак не найден")
        else:
            await ctx.send("Начался сбор участников!")
            await ctx.send("Игроки могут присоединятся, написав 'si! join'\n" + 
                           "Чтобы завершить сбор игроков, напишите 'si! end'")

    @commands.command(name='join')
    async def join(self, ctx):
        if ctx.channel in self.bot.games.keys():
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
        else:
            await ctx.send(f"{error} (фича для дебага. В дальнейшем такого не будет)")


class GameSession:
    def __init__(self, pack_name, game_id):
        self.pack_name = pack_name
        self.id = game_id
        # здесь будет получение пака через API
        
        with open(f'{pack_name}.json') as f:
            self.pack = json.load(f)

        # ------

        self.members = {}
        self.joinable = True

        self.cur_round = 0

    def add_member(self, member):
        if self.joinable:
            if member in self.members.keys():
                raise ValueError(f"{member.mention}, ты уже в игре!")
            else:
                self.members[member] = 0
        else:
            raise ValueError('Сбор игроков уже завершен')

    def is_joinable(self):
        return self.joinable

    def get_members(self, names_only=False):
        return self.members.keys() if names_only else self.members

    def end_join(self):
        if self.joinable:
            if len(self.members) > 0:
                self.joinable = False
                self.cur_player = random.choice(list(self.members.keys()))
            else:
                raise ValueError('Нельзя начать игру, в которой нет игроков')
        else:
            raise ValueError('Сбор игроков уже завершен')

    def update_round(self):
        self.cur_round += 1
        self.create_table_image()
        return self.cur_round

    def get_categories(self):
        result = {}
        for category in self.pack['rounds'][self.cur_round - 1]['categories']:
            result[category['name']] = category['description']
        return result

    def create_table_image(self):
        img = Image.new("RGB", (701, len(self.pack['rounds'][self.cur_round - 1]['categories']) * 75 + 1), (0, 0, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('static/OpenSans.ttf', 35)
        for i in range(6):
            for j in range(len(self.pack['rounds'][self.cur_round - 1]['categories'])):
                if i == 0:
                    draw.rectangle([(i * 100, j * 75), ((i + 1) * 100 + 100, (j + 1) * 75)], width=2, outline=(255, 255, 0))
                    draw.text((i * 100 + 5, j * 75 + 15), self.pack['rounds'][self.cur_round - 1]['categories'][j]['name'], fill=(255, 255, 0), font=font)
                else:
                    draw.rectangle([(i * 100 + 100, j * 75), ((i + 1) * 100 + 100, (j + 1) * 75)], width=2, outline=(255, 255, 0))
                    draw.text((i * 100 + 115, j * 75 + 15), str(self.pack['rounds'][self.cur_round - 1]['categories'][j]['questions'][i - 1]['par']), fill=(255, 255, 0), font=font)

        img.save(f'temp/{self.id}.png')

    def get_image_path(self):
        return f'temp/{self.id}.png'

    def get_cur_player(self):
        return self.cur_player


bot = SiGameBot(command_prefix='si! ')
bot.add_cog(SiCommands(bot))
bot.run(TOKEN)
