import discord
from discord.ext import commands
import chess
from bot_logic import *
import os
import random
import urllib.request
import json

intents = discord.Intents.default()
intents.message_content = True

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
KEY = os.getenv('KEY_YOUTUBE')


bot = commands.Bot(command_prefix='$', intents=intents)

games = {}

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send("Hi!")

@bot.command()
async def bye(ctx):
    await ctx.send(":(")

@bot.command()
async def password(ctx):
    await ctx.send(gen_pass(10))

@bot.command()
async def smile(ctx):
    await ctx.send(gen_emodji())

@bot.command()
async def coin(ctx):
    await ctx.send(flip_coin())

@bot.command()
async def meme(ctx):
    memes = random.choice(os.listdir("images"))
    with open(f'images/{memes}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="usuario")
    await member.add_roles(role)
    await member.send(f"¡Bienvenido {member.name}! Se te ha asignado el rol {role.name}.")

@bot.command()
async def like(ctx):
    mensaje = await ctx.send("Reacciona con 👍 para obtener el rol 'like'.")
    await mensaje.add_reaction('👍')

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.emoji == '👍':
        role = discord.utils.get(user.guild.roles, name="like")
        if role:
            await user.add_roles(role)
            await user.send("¡Te hemos añadido el rol 'like'!")
        else:
            await user.send("El rol 'like' no existe. Por favor, informa al administrador.")

@bot.command(name='subs')
async def subscriptores(ctx, username):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={username}&key={KEY}"
    data = urllib.request.urlopen(url).read()
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    response = f"{username} tiene {int(subs):,d} suscriptores!"
    await ctx.send(response)

bot.run(TOKEN)
