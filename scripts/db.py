import scripts.canvas_api as canvas_api
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, date, time, timedelta

client = MongoClient("mongodb+srv://canv:Canv10@canvasusers.lzqrtdz.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.Canvas
users = db.Users
jobs = db.jobs

async def new_user(user_id: str, token: str):
    # fetch courses belonging to user
    courses = await canvas_api.getCourses(token)

    new_courses = {}
    for course in courses:
        new_courses[course] = {
            "id": courses[course],
            "notifications": False
        }
        
    userDoc = {
        '_id': user_id,
        'courses': new_courses,
        'notifications': False,
        'days': 0,
    }
    
    users.insert_one(userDoc)
    
def update_notifications(user_id: int, notifications: bool):
    users.update_one({'_id': user_id}, {'$set': {'notifications': notifications}})


def update_days(user_id: int, days: int):
    users.update_one({'_id' : user_id}, {'$set': {'days': days}})


def update_token(user_id: int, token: str):
    users.update_one({'_id': user_id}, {'$set': {'token': token}})


def update_courses(user_id: int, courses):
    users.update_one({'_id': user_id}, {'$set': {'courses': courses}})


def get_token(user_id: int):
    return users.find_one({'_id': user_id})['token']


def get_courses(user_id: int):
    return users.find_one({'_id': user_id})['courses']


def is_user(user_id: int):
    return users.find_one({'_id': user_id}) is not None


def update_assignments(user_id: int, assignments):
    users.update_one({'_id': user_id}, {'$set': {'assignments': assignments}})


def delete_user(user_id: int):
    users.delete_one({'_id': user_id})
