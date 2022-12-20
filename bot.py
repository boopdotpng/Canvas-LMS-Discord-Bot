from dotenv import load_dotenv
import os
import discord
import logging
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()

if os.getenv('TESTING'):
	token = str(os.getenv("TOKEN_TEST"))
else:
	token = str(os.getenv("TOKEN"))

bot = commands.Bot(command_prefix = "@", intents=discord.Intents.default())

@bot.event
async def on_ready():
	logger.info("Startup Sequence Completed")
	test_channel =  await bot.get_channel(860332677852037153)
	await test_channel.send("Startup Sequence Completed")

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		bot.load_extension("cogs." + f[:-3])

bot.run(os.getenv("TOKEN"))