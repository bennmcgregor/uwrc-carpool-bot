import discord
from discord.ext import commands
from custom_errors import *

def admin_validation(ctx):
    if not discord.utils.get(ctx.guild.roles, name="Carpool Admin") in ctx.author.roles:
        raise AdminValidationError()

def channel_validation(ctx):
    # TODO: don't rely on specific channel IDs (find the ID by name on startup)
    if not (isinstance(ctx.channel, discord.channel.DMChannel) or ctx.channel.name == "carpool-scheduling" or ctx.channel.name == "carpool-admin"):
        raise ChannelValidationError()

def command_validation(pred):
    if not pred():
        raise CommandValidationError()