import discord
import json
import os
import asyncio
from random import randint
from discord.ext import commands
from discord.utils import get
from config import settings

os.system("cls")

bot = commands.Bot(intents = discord.Intents.all(), command_prefix = settings['prefix'])

global membervoice
living_people = []
membervoice = []
nigh_status = 0

global void_people
global departure
void_people = []
departure = {}

global kill_people
global heal_people
kill_people = []
heal_people = []

time_to_voise = 0
speak_people = []



@bot.event
async def on_ready():
	print("Bot was connected to the server")


@bot.command()
async def cls(ctx):
	os.system("cls")

@bot.command()
async def check(ctx, member:discord.Member = None):
	global connection
	print(nigh_status)
	if ctx.channel.id != 950029272255463424:
		await ctx.send("Вы не можете убить кого-то в этом чате")
	elif living_people.count(member) == 0:
		await ctx.send("Этот игрок мертв")
	elif connection == 0:
		await ctx.send("Вы можете использовать эту команду 1 раз за раунд")
	elif nigh_status == 2:
		connection -= 1
		await ctx.send(member.roles[1].name)

@bot.command()
async def heal(ctx, member:discord.Member = None):
	if nigh_status == 0:
		await ctx.send("Сейчас нельзя кого-то спасти")
	elif living_people.count(member) == 0:
		await ctx.send("Этот игрок мертв")
	elif nigh_status == 3:
		heal_people.append(member)
		await ctx.send("Вы спасли игрока")

@bot.command()
async def void(ctx):#, member:discord.Member = None):
	if ctx.message.content.split(" ")[1] in ["скип", "s", "с", "skip"]:
		if departure.get("скип") == None:
			departure["скип"] = 1
			#departure.update(member.name=0)
		else:
			departure["скип"] = departure[member]+1
		#print(departure)
	else:
		server = bot.get_guild(id=950029039005995059)
		member = server.get_member(int(ctx.message.content.split("!")[1].replace(">", "")))
		#print(member)
		if ctx.message.author in void_people:
			await ctx.send("Ты уже голосовал")
		elif living_people.count(member) == 0:
			await ctx.send("Этот игрок мертв")
		elif nigh_status >= 1:
			await ctx.send("Сейчас нельзя голосовать")
		else:
			void_people.append(ctx.message.author)
			#print(member.name)
			if departure.get(member) == None:
				departure[member] = 1
				#departure.update(member.name=0)
			else:
				departure[member] = departure[member]+1

@bot.command()
async def kill(ctx, member:discord.Member = None):
	if member == None:
		await ctx.send("Вы должны указать игрока")
	elif living_people.count(member) == 0:
		await ctx.send("Этот игрок мертв")
	elif member == "Мафия#4365":
		await ctx.send("Вы не можете убить бота")
	elif nigh_status == 0:
		await ctx.send("Вы не можете убить во время дня")
	elif len(kill_people) >= 1:
		await ctx.send("Вы уже убили игрока\nЖдите следующей ночи")
	elif ctx.channel.id != 950029227015692328:
		await ctx.send("Вы не можете убить кого-то в этом чате")
	elif nigh_status == 1:
		if member in living_people:
			kill_status = 0
			if kill_status == 0:
				for i in living_people:
					if i == member:
						kill_people.append(i)
						#del living_people[living_people.index(i)]
						await ctx.send("Вы убили игрока")
		else:
			await ctx.send("Он уже мертв")

	#print(ctx.message.author)

@bot.command()
async def back(ctx, channel_name='Город'): #member: discord.Member,
	start_channel = bot.get_channel(950311235587559435)
	city_channel = bot.get_channel(950029039798714401)
	role0 = bot.guilds[0].get_role(950334395414368266)#Мафия
	role1 = bot.guilds[0].get_role(950330019761254400)#Доктор
	role2 = bot.guilds[0].get_role(950334540075913246)#Комиссар
	for i in city_channel.members:
		await i.edit(voice_channel=start_channel)
		await i.remove_roles(role0)
		await i.remove_roles(role1)
		await i.remove_roles(role2)
		await i.edit(mute=False)


@bot.command()
async def give_roles(ctx):
	start_channel = bot.get_channel(950311235587559435)
	city_members = start_channel.members
	scenario = 0
	if len(start_channel.members) < 5:
		scenario = 1
		role0 = bot.guilds[0].get_role(950334395414368266)#Мафия
		role1 = bot.guilds[0].get_role(950330019761254400)#Доктор
		role2 = bot.guilds[0].get_role(950334540075913246)#Комиссар

		city_members0 = city_members[randint(0, len(city_members)-1)]
		del city_members[city_members.index(city_members0)]
		city_members1 = city_members[randint(0, len(city_members)-1)]
		del city_members[city_members.index(city_members1)]
		city_members2 = city_members[randint(0, len(city_members)-1)]

		await city_members0.add_roles(role0)
		await city_members1.add_roles(role1)
		await city_members2.add_roles(role2)

		mafia = bot.get_channel(950029227015692328)
		doctor = bot.get_channel(950029301024186408)
		komissar = bot.get_channel(950029272255463424)
		await mafia.send(f"{city_members0.mention} ты мафия")
		await doctor.send(f"{city_members1.mention} ты доктор")
		await komissar.send(f"{city_members2.mention} ты комисар")

	else:
		scenario = 2
		role0 = bot.guilds[0].get_role(950334395414368266)#Мафия
		role1 = bot.guilds[0].get_role(950330019761254400)#Доктор
		role2 = bot.guilds[0].get_role(950334540075913246)#Комиссар
		
		city_members0 = city_members[randint(0, len(city_members)-1)]
		del city_members[city_members.index(city_members0)]

		city_members00 = city_members[randint(0, len(city_members)-1)]
		del city_members[city_members.index(city_members00)]

		city_members1 = city_members[randint(0, len(city_members)-1)]
		del city_members[city_members.index(city_members1)]

		city_members11 = city_members[randint(0, len(city_members)-1)]
		del city_members[city_members.index(city_members11)]

		city_members2 = city_members[randint(0, len(city_members)-1)]
		del city_members[city_members.index(city_members2)]
		city_members22 = city_members[randint(0, len(city_members)-1)]

		await city_members0.add_roles(role0)
		await city_members00.add_roles(role0)
		await city_members1.add_roles(role1)
		await city_members2.add_roles(role2)

		mafia = bot.get_channel(950029227015692328)
		doctor = bot.get_channel(950029301024186408)
		komissar = bot.get_channel(950029272255463424)
		await mafia.send(f"{city_members0.mention} и {city_members00.mention} вы мафия")
		await doctor.send(f"{city_members1.mention} ты доктор")
		await komissar.send(f"{city_members2.mention} ты комисар")


@bot.command()
async def skip(ctx):
	global time_to_voise
	if ctx.message.author == speak_people: time_to_voise = 0
	print(time_to_voise)
	#print(if ctx.message.author == speak_people: time_to_voise = 0)

@bot.command()
async def start(ctx, channel_name='Город'): #member: discord.Member,
	global nigh_status
	global connection
	global time_to_voise
	global speak_people
	connection = 1
	start_channel = bot.get_channel(950311235587559435)
	city_channel = bot.get_channel(950029039798714401)
	#between_channel = bot.get_channel(956629660656083044)
	if len(start_channel.members) < 5:
		await ctx.send("Игроков меньше 5\nИгра не начнеться", tts=True)
	else:

		await ctx.send("Начинается выдача ролей", tts=True)

		await give_roles(ctx)

		await ctx.send("Игра начнется через пару секунд", tts=True)

		role = bot.guilds[0].get_role(950323207292985437)#игрок
		role0 = bot.guilds[0].get_role(950334395414368266)#Мафия
		role1 = bot.guilds[0].get_role(950334540075913246)#Комисар
		role2 = bot.guilds[0].get_role(950330019761254400)#Доктор
		for i in start_channel.members:
			#print(i)
			await i.edit(voice_channel=city_channel)
			await i.add_roles(role)
			await i.edit(mute=True)

		await ctx.send("Участники игры были перемещены в Город", tts=True)

		global living_people
		global kill_people
		global heal_people

		n = 3
		msg = await ctx.send(f"Настройки завершены\nИгра начнется через {n} секунд", tts=True)
		while n > -1: 
			await msg.edit(content=f"Настройки завершены\nИгра начнется через {n} секунд")
			await asyncio.sleep(1)
			n -= 1

		roleID = 950334395414368266
		role = get(ctx.guild.roles, id = roleID)
		print(f'Список пользователей для роли "{role.name}"\n')
		number = 0
		for member in role.members:
			number += 1
			print(f'№: {number}\nName: {member.name}\nID: {member.id}\nDiscriminator: {member.discriminator}\nStatus: {member.status}\n')
			

		living_people = bot.get_channel(950029039798714401).members

		#for i in living_people:
			#print(i.roles)

		day = 0
		night = 0
		game = True

		for i in living_people:
			await i.edit(mute=True)

		for i in living_people:
			speak_people = i
			time_to_voise = 120
			await i.edit(mute=False)
			await ctx.send(f"Слово предоставляется игроку {i.mention}", tts=True)
			msg = await ctx.send(f"Осталось {time_to_voise} секунд")
			while time_to_voise > -1: 
				await msg.edit(content=f"Осталось {time_to_voise} секунд")
				await asyncio.sleep(1)
				time_to_voise -= 1
			await i.edit(mute=True)
			speak_people = []

		while game:
			print(living_people[0])
			living_people.append(living_people[0])
			living_people.pop(0)
			#	for i in living_people:
			#		i.roles
			await ctx.send(f"Наступает ночь № {night}\nГород засыпает, просыпается мафия\n(Мафия, прошу вас перейти в свой чат)\n@everyone ", tts=True)

			await ctx.send(f"Обьявляю минуту мафии", tts=True)
			nigh_status = 1
			n = 60
			msg = await ctx.send(f"Осталось {n} секунд")
			while n > -1: 
				await msg.edit(content=f"Осталось {n} секунд")
				await asyncio.sleep(1)
				n -= 1

			await ctx.send(f"Обьявляю минуту Комиссара", tts=True)
			nigh_status = 2
			if connection != 1:
				connection += 1
			n = 60
			msg = await ctx.send(f"Осталось {n} секунд")
			while n > -1: 
				await msg.edit(content=f"Осталось {n} секунд")
				await asyncio.sleep(1)
				n -= 1

			await ctx.send(f"Обьявляю минуту Доктора", tts=True)
			nigh_status = 3

			n = 60
			msg = await ctx.send(f"Осталось {n} секунд")
			while n > -1: 
				await msg.edit(content=f"Осталось {n} секунд")
				await asyncio.sleep(1)
				n -= 1

			night += 1

			await ctx.send(f"Наступает день № {day}\nГород просыпается\n@everyone", tts=True)

			if len(kill_people) > 0:
				if not heal_people:
					del living_people[living_people.index(kill_people[0])]
					await ctx.send(f"{kill_people[0].mention} больше не проснется :(", tts=True)
				else:
					if heal_people != kill_people[0]:
						del living_people[living_people.index(kill_people[0])]
						await ctx.send(f"{kill_people[0].mention} больше не проснется :(", tts=True)
					else:
						await ctx.send(f" Никто не умер этой ночью :)", tts=True)


				kill_people = []
				heal_people = []

			nigh_status = 0
			day += 1


			for i in living_people:
				speak_people = i
				time_to_voise = 120
				await i.edit(mute=False)
				await ctx.send(f"Слово предоставляется игроку {i.mention}", tts=True)
				msg = await ctx.send(f"Осталось {time_to_voise} секунд")
				while time_to_voise > -1: 
					await msg.edit(content=f"Осталось {time_to_voise} секунд")
					await asyncio.sleep(1)
					time_to_voise -= 1
				await i.edit(mute=True)
				speak_people = []


			await ctx.send(f"Голосование началось\n@everyone")
			n = 60
			msg = await ctx.send(f"Осталось {n} секунд")
			while n > -1: 
				await msg.edit(content=f"Осталось {n} секунд")
				await asyncio.sleep(1)
				n -= 1

			await ctx.send(f"Подсчет голосов", tts=True)
			#print(max(departure, key=departure.get))
			if not departure:
				await ctx.send(f"Никто не проголосовал", tts=True)
			elif departure[max(departure, key=departure.get)] < 1:
				await ctx.send(f"Недостаточно голосов", tts=True)
			else:
				await ctx.send(f"{max(departure, key=departure.get).mention} покидает игру", tts=True)
				del living_people[living_people.index(max(departure, key=departure.get))]

			game = False
			text = "Мафия проиграла"

			roleID = 950334395414368266
			role = get(ctx.guild.roles, id = roleID)
			number = 0
			for member in role.members:
				if member in living_people: number += 1

			if number > 0 and len(living_people) > 2:
				game = True
			elif number > 0 and len(living_people) < 3:
				text = "Мафия победила"
				#break
			elif number < 1 and len(living_people) > 2:
				game = False
			if game == False:
				await ctx.send(text)
				for i in city_channel.members:
					await i.edit(voice_channel=start_channel)
					await i.remove_roles(role0)
					await i.remove_roles(role1)
					await i.remove_roles(role2)
					await i.edit(mute=False)
			
@bot.command()
async def dr(ctx):
	start_channel = bot.get_channel(950311235587559435)
	role0 = bot.guilds[0].get_role(950334395414368266)#Мафия
	role1 = bot.guilds[0].get_role(950334540075913246)#Комисар
	role2 = bot.guilds[0].get_role(950330019761254400)#Доктор
	for i in start_channel.members:
		await i.remove_roles(role0)
		await i.remove_roles(role1)
		await i.remove_roles(role2)
		await i.edit(mute=False)


@bot.command(name="clear", brief="очистить чат", usage="clear")#декоратор - так называемый "фантик"
async def clear(ctx, amount = 100):#функция которая выполняется если бот получит команду - "начало конфетки"
	await ctx.channel.purge(limit = amount)#асинхронное выполнение команды, тут мы говорим боту удалить сообщения 
										   #с лимитом 100 сообщений - середина кофетки

@bot.command(name="join", brief="Подключение к голосовому каналу", usage="join")
async def join_to_channel(ctx):
	await ctx.message.delete() #удаляет сообщение с командой
	channel = bot.guilds[0].channels[3] #в переменную записываются канал 
	voice = get(bot.voice_clients, guild = ctx.guild) #в переменную записывается голосовой канал
	if voice and voice.is_connected(): #идет проверка: если бот находиться в другом канале 
									   #- он переходит в нужный нам канал
		await voice.move_to(channel)#асинхронная команда которая говорит боту куда ему переходить
	else: #если бот не сидит в войсах, то он заходит в указаный ранее канал канал
		voice = await channel.connect()
	

@bot.command(name="leave", brief="Отключение от голосового канала", usage="leave")
async def leave_to_channel(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(bot.voice_clients, guild = ctx.guild)
	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await channel.connect()


bot.run(settings['token']) #запуск бота 
