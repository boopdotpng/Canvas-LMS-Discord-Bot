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
    userID = str(userID)
    user = user_collection.find_one({"_id": str(userID)})

    return True if user else False

async def newUser(userID, token, notify=False, notify_days=0, notify_time=datetime.strptime("5:00 pm", "%I:%M %p")):
    userID = str(userID)
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
        "notify_time": notify_time
    }

    user_collection.insert_one(user)

def updateNotify(userID, notify):
    userID = str(userID)
    user_collection.update_one({"_id": userID}, {"$set": {"notify": notify}})

def updateNotifyDays(userID, notify_days):
    userID = str(userID)
    user_collection.update_one({"_id": userID}, {"$set": {"notify_days": notify_days}})

def updateCourseSettings(userID, courses):
    userID = str(userID)
    user_collection.update_one({"_id": userID}, {"$set": {"courses": courses}})

def deleteAccount(userID):
    userID = str(userID)
    user_collection.delete_one({"_id": userID})

def getToken(userID):
    userID = str(userID)
    user = user_collection.find_one({"_id": userID})
    return user["token"]

def getCourses(userID):
    userID = str(userID)
    user = user_collection.find_one({"_id": userID})
    return user["courses"]

def updateNotifyTime(userID, time):
    userID = str(userID)
    user_collection.update_one({"_id": userID }, {"$set": {"notify_time": time}})