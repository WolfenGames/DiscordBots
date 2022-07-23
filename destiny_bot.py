import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')


from random import choice

LIST_OF_EVENTS = [
    'Nightfall Strikes',
    'Strikes',
    'Crucible',
    'Gambit',
    'Planet Bounties'
]

HELP_TEXT = """
 **Welcome to the Destiny 2 event selector bot**
 I understand certain commands such as
 * `!select event` or `!se` to select a event
"""

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content in ['!select event', '!se']:
        response = choice(LIST_OF_EVENTS)
        await message.channel.send(f'{message.author} has requested for the light to choose an event, they chose **{response}**!')

    if message.content in ['!destiny2 help', '!d2h']:
        await message.channel.send(f'{HELP_TEXT}')

client.run(TOKEN)
