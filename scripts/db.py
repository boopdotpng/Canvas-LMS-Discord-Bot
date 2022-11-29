from tinydb import TinyDB, Query
from tinydb.table import Document
import scripts.canvas_api as canvas_api
from tinydb.queries import where

db = TinyDB('db.json')
user_table = db.table('users')
server_table = db.table('servers')


async def new_user(user_id: int, token: str):
    # fetch courses belonging to user
    courses = await canvas_api.getCourses(token)

    new_courses = {}
    for course in courses:
        new_courses[course] = {
            "id": courses[course],
            "notifications": False
        }

    user_table.insert(Document({'token': token,
                                'courses': new_courses, 'notifications': False, 'days': 0}, doc_id=int(user_id)))


def update_notifications(user_id: int, notifications: bool):
    user_table.update(
        Document({'notifications': notifications}, doc_id=user_id))


def update_days(user_id: int, days: int):
    user_table.update(Document({'days': days}, doc_id=user_id))


def update_token(user_id: int, token: str):
    user_table.update(Document({'token': token}, doc_id=user_id))


def update_courses(user_id: int, courses):
    user_table.update(Document({'courses': courses}, doc_id=user_id))


def get_token(user_id: int):
    return user_table.get(doc_id=user_id)['token']


def get_courses(user_id: int):
    return user_table.get(doc_id=user_id)['courses']


def is_user(user_id: int):
    return user_table.get(doc_id=user_id) is not None


def update_assignments(user_id: int, assignments):
    user_table.update(Document({'week_assignments': assignments}, doc_id=user_id))


def delete_user(user_id: int):
    user_table.remove(doc_ids=[user_id])
