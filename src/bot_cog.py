import discord
from discord.ext import commands
from custom_errors import *
from schemas.enums import CarpoolCalculationMethod
from schemas.term_data import *
from schemas.metadata import *
from schemas.user_data import *
from validation import *
from parsing import *

def get_current_term_num():
    return MetaData.objects.first().current_term_num

def get_current_term_data():
    return TermData.objects(term_num=get_current_term_num()).first()

def get_current_user_data(term_data, ctx, get_embedded_doc=False):
    query_set = term_data.user_data.filter(user_id=ctx.author.id)
    if get_embedded_doc:
        return query_set.first()
    return query_set

class CarpoolBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-address", brief='Set your home address.')
    async def _set_address(
        self,
        ctx,
        number: int = commands.parameter(description="The street number of your house/apartment."),
        street_name: str = commands.parameter(description="The street name. Wrap with quotation marks, e.g. \"Main St\""),
        city: str = commands.parameter(description="The city. Wrap with quotation marks, e.g. \"King City\"")
    ):
        channel_validation(ctx)
        command_validation(lambda: number > 0 and street_name != "" and city != "")
        # TODO: validate the existence of the address. Have appropriate error messages (raise an AddressValidationError)
            # Automatically add the province (Ontario) and country to the query
        address_data = AddressData(number=number, street=street_name, city=city)

        term_data = get_current_term_data()
        get_current_user_data(term_data, ctx, True).address_data = address_data
        term_data.save()
        await ctx.send(f'Successfully updated your address.')
    
    @commands.command(name="set-practice-availability-all", brief='Change your practice availability.', description='Join or cancel on every practice at once.')
    async def _set_avail_all(
        self,
        ctx,
        attendance: str = commands.parameter(description="Must be either `join` or `cancel`."),
    ):
        channel_validation(ctx)
        command_validation(lambda: attendance in ["join", "cancel"])
        joining = attendance == "join"
        # TODO: join all practices or cancel all practices
        await ctx.send(f'Successfully updated your availability')
    
    @commands.command(name="set-practice-availability-by-weekdays", brief='Change your practice availability.', description='Select the weekdays you are available to join or cancel on practice.\nFor the availability argument, provide the parameters in the form `prac1 [1-7] prac2 [1-7]`, where [1-7] represents a possibly empty sequence of the numbers 1 through 7, where 1 = Monday, 2 = Tuesday, etc. Examples of valid commands include `set-practice-availability-by-weekdays join prac1 135 prac2 246` or `set-practice-availability-by-weekdays cancel prac1 prac2 1234567`.')
    async def _set_avail_weekdays(
        self,
        ctx,
        attendance: str = commands.parameter(description="Must be either `join` or `cancel`."),
        *,
        availability: str = commands.parameter(description="Must be of the format `prac1 [1-7] prac2 [1-7]`.")
    ):
        channel_validation(ctx)
        command_validation(lambda: attendance in ["join", "cancel"])
        prac1s, prac2s = parse_prac1_prac2_weekdays(availability)
        joining = attendance == "join"
        # TODO: update relevant db fields and join practices
        await ctx.send(f'Successfully updated your availability.')
        await ctx.send(f"See: {joining}\n{prac1s}\n{prac2s}")
    
    @commands.command(name="set-practice-availability-by-dates", brief='Change your practice availability.', description='Select the dates you are available to join or cancel on practice.\nFor the availability argument, provide the parameters in the form `[ddmmyy prac1|prac2]*`, where prac1|prac2 represents the combinations `prac1`, `prac2`, and `prac1prac2`, and ddmmyy is the date of the practice in question. The `*` means you can repeat the sequence in brackets between 1 and infinite times. Examples of a valid command is `set-practice-availability-by-dates join 010123 prac1prac2 020123 prac2`.')
    async def _set_avail_dates(
        self,
        ctx,
        attendance: str = commands.parameter(description="Must be either `join` or `cancel`."),
        *,
        availability: str = commands.parameter(description="Must be of the format `[ddmmyy prac1|prac2]*`.")
    ):
        channel_validation(ctx)
        command_validation(lambda: attendance in ["join", "cancel"])
        date_list = parse_multiple_dates(availability)
        joining = attendance == "join"
        # TODO: update relevant db fields and join practices
        await ctx.send(f'Successfully updated your availability.')
        await ctx.send(f"See: {joining}\n{date_list}")
    
    @commands.command(name="set-car", brief='Register to be a driver of carpools.')
    async def _set_car(
        self,
        ctx,
        num_seats: int = commands.parameter(description="Must be a number between 2 and 8 inclusive."),
        description: str = commands.parameter(description="Must wrap with quotation marks. E.g. \"Red Honda Civic\".")
    ):
        channel_validation(ctx)
        command_validation(lambda: num_seats in range(1, 9) and description != "")

        car_data = CarData(num_seats=num_seats, description=description)

        term_data = get_current_term_data()
        get_current_user_data(term_data, ctx, True).car_data = car_data
        term_data.save()
        await ctx.send(f'Successfully updated your car data. You are now designated as a driver for every practice you can attend.')
    
    @commands.command(name="remove-car", brief='Cancel being a driver of carpools.')
    async def _remove_car(self, ctx):
        channel_validation(ctx)
        term_data = get_current_term_data()
        get_current_user_data(term_data, ctx, True).car_data = None
        term_data.save()
        await ctx.send(f'Successfully removed your car data. Now you will no longer be designated as a driver.')
    
    @commands.command(name="set-practice-availability-admin-all", brief='Change all users\' practice availability.', description='Change all users\' availability for a single practice. Only available to admins.\nFor the date argument, provide the parameter in the form `ddmmyy`, where ddmmyy is the date of the practice in question.\nFor the practice_type argument, provide the parameter in the form `prac1|prac2`, representing the possible combinations `prac1`, `prac2`, and `prac1prac2`.\nAn example command would be `set-practice-availability-admin-all join 010123 prac1prac2`.')
    async def _set_avail_admin_all(
        self,
        ctx,
        attendance: str = commands.parameter(description="Must be either `join` or `cancel`."),
        date: str = commands.parameter(description="Must be of the format `ddmmyy`."),
        practice_type: str = commands.parameter(description="Must be of the format `prac1|prac2`.")
    ):
        admin_validation(ctx)
        channel_validation(ctx)
        command_validation(lambda: attendance in ["join", "cancel"])
        date = parse_single_date(date + " " + practice_type)
        joining = attendance == "join"
        # TODO: join practice and add every non-Inactive user as an attendee
        await ctx.send(f'Successfully updated every member\'s availability')
    
    @commands.command(name="set-practice-availability-admin-by-user", brief='Change a user\'s practice availability.', description='Change a specific user\'s availability for a single practice. Only available to admins.\nFor the date argument, provide the parameter in the form `ddmmyy`, where ddmmyy is the date of the practice in question.\nFor the practice_type argument, provide the parameter in the form `prac1|prac2`, representing the possible combinations `prac1`, `prac2`, and `prac1prac2`.\nFor the `users` argument, provide a space-separated list of server usernames to add to/remove from the given practice.\nAn example command would be `set-practice-availability-admin-by-user join 010123 prac1prac2 @bobuser @noninactivemember`.')
    async def _set_avail_admin_user(
        self,
        ctx,
        attendance: str = commands.parameter(description="Must be either `join` or `cancel`."),
        date: str = commands.parameter(description="Must be of the format `ddmmyy`."),
        practice_type: str = commands.parameter(description="Must be of the format `prac1|prac2`."),
        *users: discord.User
    ):
        admin_validation(ctx)
        channel_validation(ctx)
        command_validation(lambda: attendance in ["join", "cancel"])
        date = parse_single_date(date + " " + practice_type)
        joining = attendance == "join"
        # TODO: join practice and add every non-Inactive user as an attendee
        await ctx.send(f'Successfully updated specific members\' availability')

    @commands.command(name="set-car-admin", brief='Update the size of a driver\'s car.')
    async def _set_car_admin(
        self,
        ctx,
        user: discord.User = commands.parameter(description="@username of someone on the server who's registered as a driver."),
        num_seats: int = commands.parameter(description="Must be a number."),
    ):
        admin_validation(ctx)
        channel_validation(ctx)
        if get_current_term_data().user_data.filter(user_id=user.id).first().car_data == None:
            raise NonexistentCarError()

        term_data = get_current_term_data()
        get_current_user_data(term_data, ctx, True).car_data.num_seats = num_seats
        term_data.save()
        await ctx.send(f'Successfully updated the number of seats for {user.name}\'s car.')

    @commands.command(name="set-carpool-logic-admin", brief='Set logic for carpool calculation')
    async def _set_carpool_logic_admin(
        self,
        ctx,
        no_varsity_in_novice: bool = commands.parameter(description="True if varsity athletes should not ride in novice cars.")
    ):
        admin_validation(ctx)
        channel_validation(ctx)
        
        meta_data = MetaData.objects.first()
        if no_varsity_in_novice:
            meta_data.carpool_calculation_method = CarpoolCalculationMethod.NO_VARSITY_IN_NOVICE
        else:
            meta_data.carpool_calculation_method = CarpoolCalculationMethod.VARSITY_IN_NOVICE
        meta_data.save()
        await ctx.send(f'Successfully updated the carpool logic.')
    

            
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, BaseBotError):
            await ctx.send(error.get_err_text(ctx))
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'ERROR: Something went wrong with your command invocation.\nThe error message is: `{error}`\nSend the command `!help` or `!help command-name` for more information on how to use the carpool bot commands.')
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')








    @commands.command(name="temp-create-metadata")
    async def _temp_create_metadata(
        self,
        ctx
    ):
        metadata = MetaData(current_term_num=1)
        metadata.save()
        await ctx.send(f"Added new metadata")

    @commands.command(name="temp-create-term")
    async def _temp_create_term(
        self,
        ctx
    ):
        term = TermData(term_num=1)
        term.save()
        await ctx.send(f"Added new term")

    @commands.command(name="temp-reg-user")
    async def _temp_reg_user(
        self,
        ctx
    ):
        for term in TermData.objects:
            if term.term_num == 1:
                # TODO: create user entry
                user_data = UserData(user_id=ctx.author.id)
                term.user_data.append(user_data)
                term.save()
                await ctx.send(f"added new UserData object for user {ctx.author.name}")
            for user in term.user_data:
                if user.user_id == ctx.author.id:
                    await ctx.send(f"verifying that the data was indeed added: {user.user_id}")