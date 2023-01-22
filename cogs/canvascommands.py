import discord
from discord.ext import commands
from scripts import canvas_api, db


class canvas_commands(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    #! show assignments for the week
    @commands.slash_command(
        name="show_week",
        description="Show the current week of assignments",
        guild_ids=[1038598934265864222]
    )
    async def show_week(self, ctx):
        userid = ctx.author.id.__int__()
        if not db.isUser(userid):
            return await ctx.respond("You do not have an account!", ephemeral=True)

        courses = db.getCourses(userid)

        assignments = await canvas_api.getWeekAssignments(db.getToken(userid), courses)

        #! work in progress
        embed = discord.Embed(
            title="Assignments",
            description="Here are your assignments for the week:",
            color=discord.Colour.brand_red()
            )

        # format & print assignments
        print(assignments)

    #! fetches user's grades
    @commands.slash_command(
        name="get_grades",
        description="get your grades",
        guild_ids=[1038598934265864222]
    )
    async def get_grades(self, ctx):
        userid = ctx.author.id.__int__()
        if not db.isUser(userid):
            return await ctx.respond("You do not have an account!", ephemeral=True)

        # get courses
        token = db.getToken(userid)
        courses = db.getCourses(userid)
        # get grades
        grades = await canvas_api.getGrades(courses, token)

        embed = discord.Embed(
            title="Grades",
            description="Your current grades",
            colour=discord.Colour.dark_gold()
        )

        for item in grades:
            embed.add_field(name=item["course"], value=str(
                item["grade"])+"%", inline=False)

        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(canvas_commands(bot))
