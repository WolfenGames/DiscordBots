import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')


from random import choice

LIST_OF_MAPS = [
    'Tanglewood Street House',
    'Ridgeview Road House',
    'Bleasdale Farmhouse',
    'Grafton Farmhouse',
    'Edgefield Street House',
    'Willow Street House',
    'Maple Lodge Campsite'
]

DIFFICULTY = [
    'Amateur',
    'Intermediate',
    'Professional',
    'Nightmare'
]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content in ['!select map', '!sm']:
        response = choice(LIST_OF_MAPS)
        await message.channel.send(f'{message.author} has requested the ether to choose a map, and they chose **{response}**!')

    if message.content in ['!select map and difficulty', '!smd']:
        response = choice(LIST_OF_MAPS)
        difficulty = choice(DIFFICULTY)
        await message.channel.send(f'_{message.author}_ has requested the ether to choose a map, and they chose **{response}** with difficulty of **{difficulty}**!')

    if message.content in ['!select difficulty', '!sd']:
        difficulty = choice(DIFFICULTY)
        await message.channel.send(f'_{message.author}_ has requested the ether to choose difficulty, and they chose a difficulty of **{difficulty}**!')


client.run(TOKEN)
