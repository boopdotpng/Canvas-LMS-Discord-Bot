# Canvas LMS Discord Bot

## About this project
This bot uses the Canvas LMS API to fetch your upcoming assignments, grades, and other information to create a canvas experience in discord.


## Getting Started
Create a virtual environment using
    python3 -m venv bot-env

or any other name you choose. Then, install the dependencies.

    python3 -m pip install -r requirements.txt

This project makes use of a .env file to store your personal discord token. Simply make a file called .env and set the variable "TOKEN" to your token.

    python3 bot.py

will start the bot on your server.

## Roadmap

- [] Show assignments command / embed visual
- [] Direct message reminders for users on the days that they specify
- [] Custom reminder times
- [] Relate server channels to courses and post new assignments in the channel
- [] Special admin settings for owner of server/bot