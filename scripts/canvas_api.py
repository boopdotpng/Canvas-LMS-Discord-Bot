import requests
from datetime import datetime, timedelta
import grequests

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

async def get_week_assignments(coursedict, token, time):
    header = {'Authorization': 'Bearer ' + token}
    data = {
        "per_page": 15,
        "bucket": "upcoming",  # only retrieve upcoming assignments
        "order_by": "due_at"
    }
    assignments = []
    time_now = datetime.now()
    time_week = time_now + timedelta(days=7)
    r = requests.get(f"https://canvas.instructure.com/api/v1/users/self/todo",
                     headers=header, data=data).json()


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
