from dotenv import load_dotenv
import os
import scripts.canvas_api as canvas_api
from pymongo import MongoClient
from datetime import datetime, date, time, timedelta


load_dotenv("../.env") #! load environment variable from root

conn = os.getenv("CONN")

client = MongoClient(conn)

maindb = client["canvas-users"]
user_collection = maindb["users"] #! each document is a user

def isUser(userID):
    user = user_collection.find_one({"_id": userID})

    return True if user else False

async def newUser(userID, token, notify=False, notify_days=0):
    # check if user already exists
    if isUser(userID):
        # update token
        user_collection.update_one({"_id": userID}, {"$set": {"token": token}})
        return

    courses = await canvas_api.getCourses(token)

    user = {
        "_id": userID,
        "token": token,
        "notify": notify,
        "courses": courses,
        "notify_days": notify_days,
    }

    user_collection.insert_one(user)

def updateNotify(userID, notify):
    user_collection.update_one({"_id": userID}, {"$set": {"notify": notify}})

def updateNotifyDays(userID, notify_days):
    user_collection.update_one({"_id": userID}, {"$set": {"notify_days": notify_days}})

def updateCourseSettings(userID, courses):
    user_collection.update_one({"_id": userID}, {"$set": {"courses": courses}})

def deleteAccount(userID):
    user_collection.delete_one({"_id": userID})

def getToken(userID):
    user = user_collection.find_one({"_id": userID})
    return user["token"]

def getCourses(userID):
    user = user_collection.find_one({"_id": userID})
    return user["courses"]
