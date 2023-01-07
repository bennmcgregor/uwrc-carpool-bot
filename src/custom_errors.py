from abc import abstractmethod
from discord.ext import commands

class BaseBotError(commands.CommandError):
    @abstractmethod
    def get_err_text(self, ctx):
        pass

class AdminValidationError(BaseBotError):
    def get_err_text(self, ctx):
        return 'ERROR: This command can only be invoked by server members with the `Carpool Admin` role.'

class ChannelValidationError(BaseBotError):
    def get_err_text(self, ctx):
        return 'ERROR: It looks like you attempted to invoke a command in the wrong channel. Either DM me or write your command in the #carpool-scheduling channel.'

class CommandValidationError(BaseBotError):
    def get_err_text(self, ctx): 
        return f'ERROR: Incorrect command invocation. Send the command `!help {ctx.command.name}` for more information on how to use this command.'

class AddressValidationError(BaseBotError):
    def get_err_text(self, ctx):
        return f'ERROR: The address you provided could not be found in Ontario, Canada. Please check your spelling and try again. See `!help {ctx.command.name}` for more information.'

class NonexistentCarError(BaseBotError):
    def get_err_text(self, ctx):
        return f'ERROR: The user mentioned does not have a car registered with the carpool bot. You must ask them to register a car before you can run this command. See `!help {ctx.command.name}` for more information.'
