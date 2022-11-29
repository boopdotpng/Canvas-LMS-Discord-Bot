import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from scripts import canvas_api, db


class canvas_commands(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    @commands.slash_command(
        name="show_week",
        description="Show the current week of assignments",
        guild_ids=[1038598934265864222]
    )
    async def show_week(self, ctx):
        userid = ctx.author.id.__int__()
        if not db.is_user(userid):
            return await ctx.respond("You do not have an account!", ephemeral=True)

        # get courses
        courses = db.get_courses(userid)
        # get assignments
        assignments = await canvas_api.getAssignments(userid, courses)
        # send message
        await ctx.respond(assignments, ephemeral=True)

    @commands.slash_command(
        name="get_grades",
        description="get your grades",
        guild_ids=[1038598934265864222]
    )
    async def get_grades(self, ctx):
        userid = ctx.author.id.__int__()
        if not db.is_user(userid):
            return await ctx.respond("You do not have an account!", ephemeral=True)

        # get courses
        token = db.get_token(userid)
        courses = db.get_courses(userid)
        # get grades
        grades = await canvas_api.get_grades(courses, token)

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