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

connect('carpool-bot-test')

bot = commands.Bot(command_prefix='!', intents=intents)
asyncio.run(bot.add_cog(CarpoolBot(bot)))
bot.run(TOKEN)

# @bot.event
# async def on_ready():
#     print(f'{bot.user.name} has connected to Discord!')

# class GenericValidationError(commands.CommandError):
#     pass

# class CommandValidationError(commands.CommandError):
#     pass

# def generic_validation(ctx):
#     # TODO: don't rely on specific channel IDs (find the ID by name on startup)
#     if not (isinstance(ctx.channel, discord.channel.DMChannel) or ctx.channel.id == 1045806779193376919):
#         raise GenericValidationError()

# def command_validation(pred):
#     if not pred():
#         raise CommandValidationError()

# @bot.command(name="set-car")
# async def _set_car(
#     ctx,
#     num_seats: int = commands.parameter(description="Must be a number between 2 and 8 inclusive."),
#     description: str = commands.parameter(description="Must wrap with quotation marks. E.g. \"Red Honda Civic\".")
# ):
#     generic_validation(ctx)
#     command_validation(lambda: num_seats in range(1, 9) and description != "")
#     await ctx.send(f'You passed {num_seats}, {description}')
        
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, GenericValidationError):
#         await ctx.send(f'It looks like you attempted to invoke a command in the wrong channel. Either DM me or write your command in the #carpool-scheduling channel.')
#     elif isinstance(error, CommandValidationError):
#         await ctx.send(f'ERROR: Incorrect command invocation. Send the command `!help {ctx.command.name}` for more information on how to use this command.')

# TODO: get the SetCar command working, including writing to DB (can also initialize all DB schemas)
# TODO: add SetFinalChangesDeadlineAdmin and SetReleaseTimeDeadlineAdmin commands, including validation and writing to DB
