import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

class help_commands(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_





def setup(bot):
    bot.add_cog(help_commands(bot))