import discord
from discord.ext import commands
from pymongo import MongoClient
from pymongo.database import Database 
from scripts import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.job import Job
from datetime import datetime, date, time, timedelta
from pytz import timezone

import logging

logger = logging.getLogger('discord')

class Scheduler(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot: commands.bot.Bot = bot_
        self.MongoClient = db.getClient()
        self.db: Database = self.mongoClient["Canvas"]
        
        self.jobstore = MongoDBJobStore(database="Canvas", collection="Jobs", client=self.mongoClient)
        self.executor = AsyncIOExecutor()
        self.scheduler = AsyncIOScheduler(jobstores={"default": self.jobstore}, executors={"default": self.executor}, timezone="America/New_York")
        
        logger.info('cogs.Scheduler: Cog intialized')
    
    def sendReminder(self, userId: int):    
        pass
    
    def addReminder(self, userId: int, weekday: int, time: time):
        user = self.bot.get_user(userId)
        
        #Generate a datetime object for the next time the reminder should be sent
        nextRunTime = datetime.combine(date.today() + timedelta(days=(weekday - date.today().weekday()) % 7), time)
        
        
        job = Job(
            scheduler=self.scheduler,
            name = f'{user.name}: {weekday} at {time.__repr__()}',
            func = self.sendReminder,
            args = [userId],
            trigger = CronTrigger(day_of_week=weekday, hour=time.hour, minute=time.minute, timezone='America/New_York'),
            executor = 'default',
            next_run_time = nextRunTime,
            misfire_grace_time = None,
            coalesce = True,
        )
        
        self.jobstore.add_job(job)
        logger.info(f'cogs.Scheduler: Added reminder for {user.name} at {time} on {weekday}')
        
    def removeReminder(self, userId: int, weekday: int, time: time):
        user = self.bot.get_user(userId)
        job: Job = self.jobstore.find_jobs(name=f'{user.name}: {weekday} at {time.__repr__()}')
        self.jobstore.remove_job(job.id)
        logger.info(f'cogs.Scheduler: Removed reminder for {user.name} at {time} on {weekday}')
        