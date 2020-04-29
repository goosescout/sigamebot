import discord
import os
import json
import pymorphy2
import random
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap


load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


class SiGameBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.games = {}

    async def on_message(self, message):
        if message.content.startswith('si! '):
            await self.process_commands(message)
        elif message.channel in self.games.keys() and self.games[message.channel].get_author_requested() == message.author:
            try:
                self.games[message.channel].init_question(message.content.split()[0], int(message.content.split()[1]))
                await self.ask_question(message.channel)
            except ValueError:
                await message.channel.send("Такого вопроса или категории не существует")
            except IndexError:
                await message.channel.send("Недостаточно аргументов")
            except Exception as ex:
                await message.channel.send(ex)
        elif message.channel in self.games.keys() and self.games[message.channel].get_race_requested() and message.content.strip().lower() == 'si!' and self.games[message.channel].is_member(message.author):
            if message.author in self.games[message.channel].get_forbidden():
                await message.channel.send(f"{message.author.mention}, вы уже отвечали")
            else:
                self.games[message.channel].cur_ans_player = message.author
                self.games[message.channel].race_requested = False
                await self.answer_question(message.channel)
        elif message.channel in self.games.keys() and not self.games[message.channel].get_race_requested() and self.games[message.channel].get_ans_player() == message.author:
            cur_game = self.games[message.channel]
            if cur_game.answer(message.content):
                await message.add_reaction('✅')
                await message.channel.send(f"Это правильный ответ! {cur_game.get_cur_question()['par']} очков игроку {cur_game.get_ans_player().mention}!")
                if cur_game.reset():
                    await self.show_questions(message.channel, True)
                else:
                    await self.show_questions(message.channel)
            else:
                await message.add_reaction('❌')
                await message.channel.send(f"К сожалению, это неправильный ответ. {cur_game.get_ans_player().mention} теряет {cur_game.get_cur_question()['par']} очков.")
                await self.post_answer(message.channel)

    async def post_answer(self, channel, case_1=False):
        cur_game = self.games[channel]
        if cur_game.get_forbidden() == list(cur_game.get_members()) or case_1:
            await channel.send("Никто не ответил на вопрос. Вопрос снимается.")
            cur_game.make_answer_pict()
            await channel.send(f"Правильный ответ был: {cur_game.get_questions_ans()}", file=discord.File(cur_game.get_answer_path()))
            if cur_game.reset():
                await self.show_questions(channel, True)
            else:
                await self.show_questions(channel)
        else:
            await channel.send("Кто первый из игроков напишет 'si!' - тот и будет отвечать!")
            self.games[channel].cur_ans_player = None
            cur_game.race_requested = True
            await self.countdown(channel)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="SiGame"))

    async def show_questions(self, channel, start=False):
        cur_game = self.games[channel]
        members = cur_game.get_members()
        str_members = '\n'.join(map(lambda x: '• ' + str(x[0].mention) + ' - ' + str(x[1]), members.items()))
        if start:
            cur_game.update_round()
            categories = cur_game.get_categories()
            str_categories = '\n'.join(map(lambda x: '• ' + x[0] + ' - ' + x[1], categories.items()))
            await channel.send(f"Начинается {cur_game.get_cur_round() + 1} раунд\n" +
                               f"Категории раунда:\n{str_categories}", file=discord.File(cur_game.get_image_path()))
        else:
            await channel.send(f"Идёт {cur_game.get_cur_round() + 1} раунд\n", file=discord.File(cur_game.get_image_path()))
        await channel.send(f"Баллы игроков:\n{str_members}\n" +
                           f"{cur_game.get_cur_player().mention}, ваш ход\n" +
                           "Вам необходимо выбрать категорию. Для этого введите: 'название категории' 'номинал вопроса' (регистр не учитывается)")
        cur_game.author_requested = cur_game.get_cur_player()
        
    async def ask_question(self, channel):
        cur_game = self.games[channel]
        cur_game.author_requested = None
        morph = pymorphy2.MorphAnalyzer()
        word = morph.parse('секунда')[0]
        await channel.send(f"Играем категорию {cur_game.get_cur_category(True)} за {cur_game.get_cur_question()['par']}!\n" +
                           f"Внимание, вопрос: {cur_game.get_cur_question(True)}", file=discord.File(cur_game.get_question_path()))
        await channel.send(f"Ответы принимаются через {cur_game.get_cur_question()['answer_time']} {word.make_agree_with_number(cur_game.get_cur_question()['answer_time']).word}.")
        await asyncio.sleep(cur_game.get_cur_question()['answer_time'])
        await channel.send("Время вышло!\nКто первый из игроков напишет 'si!' - тот и будет отвечать!")
        cur_game.race_requested = True
        await self.countdown(channel)

    async def countdown(self, channel):
        cur_game = self.games[channel]
        cur_game.countdown_num += 1
        my_num = cur_game.countdown_num
        my_question = cur_game.get_cur_question()
        await asyncio.sleep(5)
        if cur_game.cur_ans_player is None and cur_game.countdown_num == my_num and my_question == cur_game.get_cur_question():
            await self.post_answer(channel, True)

    async def answer_countdown(self, channel):
        cur_game = self.games[channel]
        my_question = cur_game.get_cur_question()
        await asyncio.sleep(25)
        if not cur_game.get_race_requested() and cur_game.get_ans_player() and my_question == cur_game.get_cur_question():
            await channel.send(f"{cur_game.get_ans_player().mention}, у вас осталось 5 секунд.")
            await asyncio.sleep(5)
        if not cur_game.get_race_requested() and cur_game.get_ans_player() and my_question == cur_game.get_cur_question():
            await channel.send(f"{cur_game.get_ans_player().mention}, вы не ответили на вопрос. {cur_game.get_ans_player().mention} теряет {cur_game.get_cur_question()['par']} очков.")
            cur_game.forbid_to_ans(cur_game.get_ans_player())
            await self.post_answer(channel)

    async def answer_question(self, channel):
        cur_game = self.games[channel]
        await channel.send(f"{cur_game.cur_ans_player.mention} отвечает!\n(Введите ваш ответ без лишних символов, у вас есть 30 секунд)")
        await self.answer_countdown(channel)
 

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
                await self.bot.show_questions(ctx.channel, True)

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
        
        with open(f'{pack_name}.json', encoding='utf-8') as f:
            self.pack = json.load(f)
            for round_ in self.pack['rounds']:
                for category in round_['categories']:
                    for question in category['questions']:
                        question['playable'] = True

        # ------

        self.members = {}
        self.joinable = True

        self.cur_round = -1
        self.author_requested = None
        self.race_requested = False
        self.cur_category = None
        self.cur_question = None
        self.cur_ans_player = None
        self.forbidden_to_ans = []
        self.countdown_num = 0
        self.answer_str = None
        self.categories_closed = 0

    def add_member(self, member):
        if self.joinable:
            if member in self.members.keys():
                raise ValueError(f"{member.mention}, ты уже в игре!")
            else:
                self.members[member] = 0
        else:
            raise ValueError('Сбор игроков уже завершен')

    def is_member(self, member):
        return member in self.members.keys()

    def is_joinable(self):
        return self.joinable

    def get_members(self, names_only=False):
        return self.members.keys() if names_only else self.members

    def get_cur_round(self):
        return self.cur_round

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
        return self.cur_round + 1

    def get_categories(self):
        result = {}
        for category in self.pack['rounds'][self.cur_round]['categories']:
            result[category['name']] = category['description']
        return result

    def create_table_image(self):
        img = Image.new("RGB", (701, len(self.pack['rounds'][self.cur_round]['categories']) * 75 + 1), (0, 0, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('static/OpenSans.ttf', 35)
        for i in range(6):
            for j in range(len(self.pack['rounds'][self.cur_round]['categories'])):
                if i == 0:
                    draw.rectangle([(i * 100, j * 75), ((i + 1) * 100 + 100, (j + 1) * 75)], width=2, outline=(255, 255, 0))
                    draw.text((i * 100 + 5, j * 75 + 15), self.pack['rounds'][self.cur_round]['categories'][j]['name'], fill=(255, 255, 0), font=font)
                else:
                    draw.rectangle([(i * 100 + 100, j * 75), ((i + 1) * 100 + 100, (j + 1) * 75)], width=2, outline=(255, 255, 0))
                    draw.text((i * 100 + 115, j * 75 + 15), str(self.pack['rounds'][self.cur_round]['categories'][j]['questions'][i - 1]['par']), fill=(255, 255, 0), font=font)

        img.save(f'temp/{self.id}.png')

    def get_image_path(self):
        return f'temp/{self.id}.png'

    def get_question_path(self):
        return f'temp/q{self.id}.png'

    def get_cur_player(self):
        return self.cur_player

    def get_author_requested(self):
        return self.author_requested

    def init_question(self, category_name, par):
        found = False
        for i, category in enumerate(self.pack['rounds'][self.cur_round]['categories']):
            if category['name'] == category_name:
                self.cur_category = category
                self.cur_category_num = i
                for j, question in enumerate(category['questions']):
                    if question['playable'] and question['par'] == par:
                        self.cur_question = question
                        self.cur_question_num = j
                        self.make_question_pict()
                        found = True
                        break
            if found:
                break
        if not found:
            raise ValueError('Такого вопроса или категории не существует')

    def get_cur_question(self, text_only=False):
        if text_only:
            return self.cur_question['text']
        else:
            return self.cur_question

    def get_cur_category(self, name_only=False):
        if name_only:
            return self.cur_category['name']
        else:
            return self.cur_category

    def make_question_pict(self):
        img = Image.new("RGB", (701, 401), (0, 0, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('static/OpenSans.ttf', 35)
        draw.rectangle([(0, 0), (700, 400)], width=2, outline=(255, 255, 0))

        lines = wrap(self.cur_question['text'], 35)
        y_text = 30
        for line in lines:
            width, height = font.getsize(line)
            draw.text(((700 - width) / 2, y_text), line, font=font, fill=(255, 255, 0))
            y_text += height

        img.save(f'temp/q{self.id}.png')

    def get_race_requested(self):
        return self.race_requested

    def get_ans_player(self):
        return self.cur_ans_player

    def answer(self, string):
        formatted_string = string.strip().lower()
        for correct_answer in self.cur_question['correct_answers']:
            if len(set(correct_answer.lower())) * 0.8 <= len(set(correct_answer.lower()) & set(formatted_string)) <= len(set(correct_answer.lower())):
                self.members[self.cur_ans_player] += self.cur_question['par']
                self.cur_player = self.cur_ans_player
                return True
        else:
            self.members[self.cur_ans_player] -= self.cur_question['par']
            self.forbid_to_ans(self.cur_ans_player)
            return False

    def forbid_to_ans(self, member):
        self.forbidden_to_ans.append(member)

    def reset(self):
        if self.cur_question:
            img = Image.open(self.get_image_path())
            draw = ImageDraw.Draw(img)
            draw.rectangle([((self.cur_question_num) * 100 + 200, self.cur_category_num * 75), ((self.cur_question_num + 1) * 100 + 200, (self.cur_category_num + 1) * 75)], width=2, outline=(255, 255, 0), fill=(0, 0, 255))
            img.save(self.get_image_path())
            self.pack['rounds'][self.cur_round]['categories'][self.cur_category_num]['questions'][self.cur_question_num]['playable'] = False
            if not any(q['playable'] for q in self.pack['rounds'][self.cur_round]['categories'][self.cur_category_num]['questions']):
                self.categories_closed += 1

        self.countdown_num = 0
        self.author_requested = None
        self.race_requested = False
        self.cur_category = None
        self.cur_question = None
        self.cur_ans_player = None
        self.forbidden_to_ans = []
        self.answer_str = None

        if len(self.pack['rounds'][self.cur_round]['categories']) == self.categories_closed:
            return True
        else:
            return False

    def get_forbidden(self):
        return self.forbidden_to_ans

    def get_questions_ans(self):
        if not self.answer_str:
            self.answer_str = random.choice(self.cur_question['correct_answers'])
        return self.answer_str

    def make_answer_pict(self):
        img = Image.new("RGB", (701, 401), (0, 0, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('static/OpenSans.ttf', 35)
        draw.rectangle([(0, 0), (700, 400)], width=2, outline=(255, 255, 0))
        
        lines = wrap(self.get_questions_ans(), 35)
        y_text = 30
        for line in lines:
            width, height = font.getsize(line)
            draw.text(((700 - width) / 2, y_text), line, font=font, fill=(255, 255, 0))
            y_text += height

        img.save(f'temp/a{self.id}.png')

    def get_answer_path(self):
        return f'temp/a{self.id}.png'


bot = SiGameBot(command_prefix='si! ')
bot.add_cog(SiCommands(bot))
bot.run(TOKEN)
