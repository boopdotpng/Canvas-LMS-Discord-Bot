import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from scripts import canvas_api, db
from discord.commands import Option
from datetime import datetime

#! update notification settings
class updateSettingsView(discord.ui.View):
    #! notis on button
    @discord.ui.button(label="On", style=discord.ButtonStyle.primary, emoji="🔔")
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message("Notifications On.", ephemeral=True)
        db.updateNotify(interaction.user.id, True)

    #! notis off button
    @discord.ui.button(label="Off", style=discord.ButtonStyle.secondary, emoji="🔕")
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("Notifications Off.", ephemeral=True)
        db.updateNotify(interaction.user.id, False)

    #! callback for course select menu | set later on
    async def course_select_callback(self, interaction):
        selected = interaction.data["values"]
        courses = db.getCourses(interaction.user.id)
        for course in selected:
            courses[course]["notifications"] = True

        db.updateCourseSettings(interaction.user.id, courses)

        return await interaction.response.send_message("Selected " + ', '.join(selected) + ".", ephemeral=True)

    #! select menu for days of week
    @discord.ui.select(
        # the placeholder text that will be displayed if nothing is selected
        placeholder="Select days",
        min_values=1,  # the minimum number of values that must be selected by the users
        max_values=7,  # the maximum number of values that can be selected by the users
        options=[  # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Sunday"
            ),
            discord.SelectOption(
                label="Monday"
            ),
            discord.SelectOption(
                label="Tuesday"
            ),
            discord.SelectOption(
                label="Wednesday"
            ),
            discord.SelectOption(
                label="Thursday"
            ),
            discord.SelectOption(
                label="Friday"
            ),
            discord.SelectOption(
                label="Saturday"
            ),
            discord.SelectOption(
                label="All"
            ),
            discord.SelectOption(
                label="Weekdays"
            )
        ]
    )

    #! days of week menu callback
    async def days_callback(self, select, interaction):
        #! bitfield conversion
        days = "0000000"
        for each in select.values:
            if each == "Sunday":
                days = "1" + days[1:]
            elif each == "Monday":
                days = days[:1] + "1" + days[2:]
            elif each == "Tuesday":
                days = days[:2] + "1" + days[3:]
            elif each == "Wednesday":
                days = days[:3] + "1" + days[4:]
            elif each == "Thursday":
                days = days[:4] + "1" + days[5:]
            elif each == "Friday":
                days = days[:5] + "1" + days[6:]
            elif each == "Saturday":
                days = days[:6] + "1"
            elif each == "All":
                days = "1111111"
            elif each == "Weekdays":
                days = "0111110"
        await interaction.response.send_message("Days selected: " + ", ".join(select.values) + ".", ephemeral=True)
        # convert days to binary
        db.updateNotifyDays(interaction.user.id, int(days, 2))

#! text input field for user to enter token
class tokenModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        #? modal defined here
        self.add_item(discord.ui.InputText(label="Enter token here: ",
                      style=discord.InputTextStyle.long, max_length=72, min_length=1, placeholder="Token"))

    #! callback for token input | token verification is done here
    async def callback(self, interaction: discord.Interaction):
        token = self.children[0].value
        isValid = canvas_api.verifyToken(token)
        if isValid[0]:
            first_name = isValid[1].split(" ")[0]
            await interaction.response.send_message(f"Welcome, {first_name}!", ephemeral=True)
            await db.newUser(interaction.user.id, token)
        else:
            await interaction.response.send_message("Invalid token", ephemeral=True)

#! button to open token input modal
class tokenButton(discord.ui.View):

    @discord.ui.button(label="Enter Token", style=discord.ButtonStyle.primary, emoji="📝")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(tokenModal(title="Token Input"))

#! delete account button view
class deleteButtonView(discord.ui.View):
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("Account deleted.", ephemeral=True)
        db.deleteAccount(interaction.user.id)

#####! the command definitions start here !#####

class setup_commands(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    def validateTime(self, time: str):
        try:
            time = datetime.strptime(time, "%I:%M %p")
            return time
        except ValueError:
            return False

    #! entry point for initial users
    @commands.slash_command(
        name="set_token",
        description="set or update your canvas token",
        guild_ids=[1038598934265864222]
    )
    async def setToken(self, ctx):
        userid = ctx.author.id.__int__()
        await ctx.respond("Please enter your token below.", view=tokenButton())

    #! adjust notification settings
    @commands.slash_command(
        name="notify_settings",
        description="customize your notification settings",
        guild_ids=[1038598934265864222]
    )
    async def updateNotify(self, ctx, time: Option(str, "Time", required=False)):
        if not db.isUser(ctx.author.id):
            return await ctx.respond("You do not have an account!", ephemeral=True)

        token = db.getToken(ctx.author.id)
        courses = db.getCourses(ctx.author.id)
        view = updateSettingsView()

        #! add course select menu to notification settings class
        # view.add_item(discord.ui.Select(
        #     placeholder="Select courses",
        #     min_values=1,
        #     max_values=len(courses),
        #     options=[discord.SelectOption(label=course)
        #              for course in courses.keys()],
        # )
        # )

        # view.children[3].callback = view.course_select_callback #! set callback to function defined in class

        await ctx.respond("Adjust notification preferences below.\n", view=view, ephemeral=True)

        time_result = self.validateTime(time)

        if time_result == False:
            await ctx.respond("Invalid time format. HH:MM pm/am", ephemeral=True)
        else:
            time_result = time_result.strftime("%I:%M %p")
            db.updateNotifyTime(str(ctx.author.id), time)
            await ctx.respond(f"Notifications will be sent at {time_result}.", ephemeral=True)

    #! delete account
    @commands.slash_command(
        name="delete_account",
        description="delete your account",
        guild_ids=[1038598934265864222]
    )
    async def deleteAccount(self, ctx):
        if not db.isUser(ctx.author.id):
            return await ctx.respond("You do not have an account!", ephemeral=True)

        await ctx.respond("Sorry to see you go! Press the button to confirm.", view=deleteButtonView(), ephemeral=True)

def setup(bot):
    bot.add_cog(setup_commands(bot))