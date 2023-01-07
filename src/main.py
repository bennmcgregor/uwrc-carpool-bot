import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from bot_cog import CarpoolBot
from mongoengine import connect

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
#TODO: add other necessary intents

# connect to DB
connect('carpool-bot-test')

bot = commands.Bot(command_prefix='!', intents=intents)
asyncio.run(bot.add_cog(CarpoolBot(bot)))
bot.run(TOKEN)
