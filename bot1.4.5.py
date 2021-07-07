from operator import itemgetter
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import datetime
import random
import json
import requests
from PIL import Image, ImageFont, ImageDraw
import io
from operator import itemgetter

Bot = commands.Bot(command_prefix="~")
@Bot.event
async def on_ready():
        print('Logged on as {0}!'.format(Bot.user))
        while True:
           await Bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Эвилкея"))
#async def on_ready():
#    guilds = await Bot.fetch_guilds(limit = None).flatten()
#    await Bot.change_presence(status = discord.Status.idle, activity= discord.Activity(name=f'за {len(guilds)} серверами. ~cmds' , type= discord.ActivityType.watching))
#    print( 'Bot connected' )


queue = []
@Bot.command()
async def bonus(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str(ctx.author.id) in money['members']:
        money['members'][str(ctx.author.id)] = {}
        money['members'][str(ctx.author.id)]['Money'] = 0
        money['members'][str(ctx.author.id)]['Status'] = "Default"
    if not str(ctx.author.id) in queue:
        if money['members'][str(ctx.author.id)]['Status'] == "Default":
            emb = discord.Embed(description=f'**{ctx.author.name}** получил награду 100 <:nameemoji:858390360480546836>', color = 0xff00ff)
            await ctx.send(embed= emb)
            money['members'][str(ctx.author.id)]['Money'] += 100
            queue.append(str(ctx.author.id))
            with open('economy.json','w') as f:
                json.dump(money,f)
            await asyncio.sleep(24*60*60)
            queue.remove(str(ctx.author.id))
        if money['members'][str(ctx.author.id)]['Status'] == "Premium":
            emb = discord.Embed(description=f'**{ctx.author.name}** получил награду 175 <:nameemoji:858390360480546836>', color = 0xff00ff)
            await ctx.send(embed= emb)
            money['members'][str(ctx.author.id)]['Money'] += 175
            queue.append(str(ctx.author.id))
            with open('economy.json','w') as f:
                json.dump(money,f)
            await asyncio.sleep(24*60*60)
            queue.remove(str(ctx.author.id))
    if str(ctx.author.id) in queue:
        emb = discord.Embed(description=f'**{ctx.author}** уже получил свою ежедневную награду', color = 0xff00ff)
        await ctx.send(embed= emb)




@Bot.command()
async def money(ctx,member:discord.Member = None):
    if member == ctx.author or member == None:
        with open('economy.json','r') as f:
            money = json.load(f)
        emb = discord.Embed(description=f'У **{ctx.author.name}** {money["members"][str(ctx.author.id)]["Money"]} <:nameemoji:858390360480546836>', color = 0xff00ff)
        await ctx.send(embed= emb)
    else:
        with open('economy.json','r') as f:
            money = json.load(f)
        emb = discord.Embed(description=f'У **{member.name}** {money["members"][str(member.id)]["Money"]} <:nameemoji:858390360480546836>', color = 0xff00ff)
        await ctx.send(embed= emb)


@Bot.command()
async def give(ctx,member:discord.Member,arg:int):
    with open('economy.json','r') as f:
        money = json.load(f)
    if money['members'][str(ctx.author.id)]['Money'] >= arg:
        emb = discord.Embed(description=f'**{ctx.author.name}** передал **{member.name}** **{arg}** <:nameemoji:858390360480546836>')
        money['members'][str(ctx.author.id)]['Money'] -= arg
        money['members'][str(member.id)]['Money'] += arg
        await ctx.send(embed = emb)
    else:
        await ctx.send('У вас недостаточно денег')
    with open('economy.json','w') as f:
        json.dump(money,f)



@Bot.command()
async def additem(ctx,role:discord.Role,cost:int,emoji:str):
    with open('economy.json','r') as f:
        money = json.load(f)
    if ctx.author.id == 323444157018275841:
        if str(role.id) in money['shop']:
            await ctx.send("Эта роль уже есть в магазине")
        if not str(role.id) in money['shop']:
            money['shop'][str(role.id)] ={}
            money['shop'][str(role.id)]['Cost'] = cost
            money['shop'][str(role.id)]['Emoji'] = emoji
            await ctx.send('Роль добавлена в магазин')
        with open('economy.json','w') as f:
            json.dump(money,f)
    if not ctx.author.id == 323444157018275841:
        await ctx.send('**У вас недостаточно прав**')


@Bot.command()
async def shop(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    emb = discord.Embed(title="Магазин \n ~buy (role)", color = 0xff00ff)
    for role in money['shop']:
        emb.add_field(name=f'{money["shop"][role]["Emoji"]} {money["shop"][role]["Cost"]}<:nameemoji:858390360480546836>',value=f'<@&{role}>',inline=True)
    await ctx.send(embed=emb)


@Bot.command()
async def removeitem(ctx,role:discord.Role):
    with open('economy.json','r') as f:
        money = json.load(f)
    if ctx.author.id == 323444157018275841:
        if not str(role.id) in money['shop']:
            await ctx.send("Этой роли нет в магазине")
        if str(role.id) in money['shop']:
            await ctx.send('Роль удалена из магазина')
            del money['shop'][str(role.id)]
        with open('economy.json','w') as f:
            json.dump(money,f)
    if not ctx.author.id == 323444157018275841:
        await ctx.send('**У вас недостаточно прав**')




@Bot.command()
async def buy(ctx,role:discord.Role):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(role.id) in money['shop']:
        if money['shop'][str(role.id)]['Cost'] <= money['members'][str(ctx.author.id)]['Money']:
            if not role in ctx.author.roles:
                await ctx.send('Вы купили роль!')
                for i in money['shop']:
                    if i == str(role.id):
                        buy = discord.utils.get(ctx.guild.roles,id = int(i))
                        await ctx.author.add_roles(buy)
                        money['members'][str(ctx.author.id)]['Money'] -= money['shop'][str(role.id)]['Cost']
            else:
                await ctx.send('У вас уже есть эта роль!')
    with open('economy.json','w') as f:
        json.dump(money,f)  


@Bot.command()
async def premium(ctx,member:discord.Member):
    with open('economy.json','r') as f:
        money = json.load(f)
    if ctx.author.id == 323444157018275841:
        emb = discord.Embed(description=f'**{member.name}** получил премиум!', color = 0xff00ff)
        money['members'][str(member.id)]['Status'] = "Premium"
        await ctx.send(embed = emb)
    with open('economy.json','w') as f:
        json.dump(money,f)

@Bot.command()
async def cmds(ctx):
    emb = discord.Embed(description=f'~author — создатель бота' '\n~info — информация о боте' '\n~companions — сервера, участвующие в партнёрской программе' '\n~partner — информация о партнёрстве \n~cmds — список доступных команд для получения информации \n~bonus — получаете ежедневный бонус. (Примечание: вы не сможете пользоваться ботом, пока не получите свой первый бонус) \n~money — ваш баланс \n~money (упомянутый человек) — узнать чей-то баланс \n~give (упомянутый человек) (сумма) —передать определённую сумму кому-либо \n~shop — магазин ролей. Если вы вместо роли видите `deleted-role`, значит эта роль продаётся на другом сервере \n~buy (упомянутая роль) — роль, которую предпочитаете купить \n~rank — ваша личная карточка \n~top — топ по балансу', color = 0xff00ff)
    await ctx.send(embed= emb)



@Bot.command()
async def author(ctx):
    await ctx.send('**ev1lk**')
@Bot.command()
async def info(ctx):
    emb = discord.Embed(description=f'**Вашему вниманию предоставляется информация о нашем проекте. Мы создали своего бота и отправили его в путешествие по множеству серверов. Проявляя активность на любом из серверов, у вас есть возможность приобрести уникальные роли сервера**', color = 0xff00ff)
    await ctx.send(embed= emb)
@Bot.command()
async def companions(ctx):
    await ctx.send('https://discord.gg/bVHHr25FXA'#мой
    '\nhttps://discord.gg/7ParAKJNPA'#фрик
    '\nhttps://discord.gg/gCcvqW2uRe') #петж
@Bot.command()
async def partner(ctx):
    await ctx.send('**По поводу сотрудничества обращаться в лс —** <@323444157018275841>')



@Bot.command()
async def top(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    x = []
    for k in range(len(money['members'])):
        array = list(money['members'])
        x.append(money['members'][array[k]]['Money'])
    for i in range(len(money['members'])-1):
        for j in range(len(money['members'])-i-1):
            if x[j] < x[j+1]:
                x[j], x[j+1] = x[j+1], x[j]
                array[j], array[j+1] = array[j+1], array[j]
    emb = discord.Embed(title="Топ", color = 0xff00ff)
    for teer in range(len(x)):
        emb.add_field(name=f'{teer+1} — {x[teer]}<:nameemoji:858390360480546836>',value=f'<@{array[teer]}> ',inline=False)
    await ctx.send(embed=emb)

messageq = []
@Bot.event
async def on_message(message):
    await Bot.process_commands(message)
    if not str(message.author.id) in messageq:
        with open('economy.json','r') as f:
            money = json.load(f)
        if len(message.content) > 10:
            money['members'][str(message.author.id)]['Money'] +=4
        messageq.append(str(message.author.id))
        with open('economy.json','w') as f:
            json.dump(money,f)
        await asyncio.sleep(5)
        messageq.remove(str(message.author.id))




@Bot.command()
async def rank(ctx):
    img = Image.new('RGBA', (345, 130), '#232529')
    url = str(ctx.author.avatar_url)[:-10]
    response = requests.get(url, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)
    img.paste(response, (15, 15, 115, 115))
    with open('economy.json','r') as f:
        money = json.load(f)
    idraw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator
    headline = ImageFont.truetype('arial.ttf',size = 25)
    undertext = ImageFont.truetype('arial.ttf', size = 15)
    rank = ImageFont.truetype('arial.ttf', size = 35)
    idraw.text((145, 15), f'{name} #{tag}', font = headline)
    idraw.text((145, 50),f'ID: {ctx.author.id}',font = undertext)
    idraw.text((145, 70),f'Balance: {money["members"][str(ctx.author.id)]["Money"]} ',font = undertext)
    idraw.text((145, 90),f'Status: {money["members"][str(ctx.author.id)]["Status"]} ',font = undertext)
    x = []
    for k in range(len(money['members'])):
        array = list(money['members'])
        x.append(money['members'][array[k]]['Money'])
    for i in range(len(money['members'])-1):
        for j in range(len(money['members'])-i-1):
            if x[j] < x[j+1]:
                x[j], x[j+1] = x[j+1], x[j]
                array[j], array[j+1] = array[j+1], array[j]    
    idraw.text((270, 70),f'#{array.index(str(ctx.author.id))+1}',font = rank, color = 0x808080)
    img.save('user_card.png')
    await ctx.send(file = discord.File(fp = 'user_card.png'))




Bot.run('ODA1MzkwNjMwMjQ3MjAyODI1.YBaMeQ.1lsjf0Y_5_6QRmI-2U3q2GgoeLY')