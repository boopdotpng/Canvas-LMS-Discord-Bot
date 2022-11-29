import requests
from datetime import datetime, timedelta
import aiohttp
current_term = "Fall 2022"


def get_user_id(token):
    header = {'Authorization': 'Bearer ' + token}
    r = requests.get(
        "https://canvas.instructure.com/api/v1/users/self", headers=header)
    r = r.json()
    return r['id']


def verifyToken(token):
    header = {'Authorization': 'Bearer ' + token}
    r = requests.get(
        "https://canvas.instructure.com/api/v1/users/self", headers=header)

    return (not r.status_code == 401, r.json()['short_name'])


def convertTime(time):
    newtime = time.replace("T", " ")
    newtime = newtime.replace("Z", "")  # ? remove excess letters

    time_object = datetime.strptime(newtime, '%Y-%m-%d %H:%M:%S')
    time_object -= timedelta(hours=5)  # ? adjust for time difference (EST)

    return time_object


def convertUrl(url):
    url = url.replace("https://canvas.instructure.com/courses/",
                      "https://uncc.instructure.com/courses/")
    return url


async def getCourses(token):
    header = {'Authorization': 'Bearer ' + token}
    data = {
        "enrollment_type": "student",
        "enrollment_state": "active",
        "per_page": 30,
        "include[]": "term"
    }
    r = requests.get(
        "https://canvas.instructure.com/api/v1/courses", headers=header, data=data).json()

    courses = []

    for i in range(len(r)-1):
        if r[i]["term"]["name"] == current_term:
            courses.append(r[i])

    courseDict = {}

    for course in courses:
        courseDict[course["name"]] = course["id"]

    return courseDict


# fetch assignments for provided courses

def get_week_assignments(token,courses=None):
    header = {'Authorization': 'Bearer ' + token}
    data = {
        "per_page": 15,
        "bucket": "upcoming",  # only retrieve upcoming assignments
        "order_by": "due_at"
    }
    assignments = []
    next_sunday = datetime.now() + timedelta(days=6 - datetime.now().weekday())
    next_sunday.replace(hour=23, minute=59, second=59, microsecond=0)

    urls = [f"https://canvas.instructure.com/api/v1/courses/{course['id']}/assignments" for course in courses.values()]





# get current grades of student
async def get_grades(courses, token):
    header = {'Authorization': 'Bearer ' + token}
    data = {
        "per_page": 15,
        "state[]": "active"
    }
    grades = []
    userID = get_user_id(token)
    r = requests.get(
        f"https://canvas.instructure.com/api//v1/users/{userID}/enrollments", headers=header, data=data)
    r = r.json()

    for course in courses.items():
        for enrollment in r:
            if enrollment['course_id'] == course[1]['id']:
                grades.append({
                    "course": course[0],
                    "grade": enrollment["grades"]['current_score']
                })
    return grades


token = "7301~WmWK83vBnf9rrxz8A9bK6DvYDmcCRIxH5zen4ApU3EarSANoupCy1Mz88Q0AzuLv"
courses = {
                "Analytical Foundations of ECE": {
                    "id": 73010000000178577,
                    "notifications": False
                },
                "Computer Organization": {
                    "id": 73010000000174979,
                    "notifications": True
                },
                "Data Structures and Algorithms C++": {
                    "id": 73010000000181288,
                    "notifications": False
                },
                "lbst": {
                    "id": 73010000000181245,
                    "notifications": True
                },
                "Logic and Networks Lab": {
                    "id": 73010000000185654,
                    "notifications": False
                },
                "Network Theory II": {
                    "id": 73010000000177080,
                    "notifications": False
                }
            }

hi = get_week_assignments(token=token, courses=courses)

print(hi)