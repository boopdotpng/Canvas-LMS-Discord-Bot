import discord
from discord.ext import commands
from scripts import canvas_api, db


class canvas_commands(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    @commands.slash_command( # shows assignments for the next week
        name="show_week",
        description="Show the current week of assignments",
        guild_ids=[1038598934265864222]
    )
    async def show_week(self, ctx):
        userid = ctx.author.id.__int__() # check if user is in database
        if not db.is_user(userid):
            return await ctx.respond("You do not have an account!", ephemeral=True)

        # get courses
        courses = db.getCourses(userid)

        # get assignments
        assignments = await canvas_api.getWeekAssignments(db.get_token(userid), courses)

        # make embed for assignments
        embed = discord.Embed(
            title="Assignments",
            description="Here are your assignments for the week:",
            color=discord.Colour.brand_red()
            )

        # format & print assignments
        print(assignments)

    @commands.slash_command( # shows current grades as in canvas
        name="get_grades",
        description="get your grades",
        guild_ids=[1038598934265864222]
    )
    async def get_grades(self, ctx):
        userid = ctx.author.id.__int__()
        if not db.isUser(userid):
            return await ctx.respond("You do not have an account!", ephemeral=True)

        # get courses/token
        token = db.get_token(userid)
        courses = db.get_courses(userid)
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
