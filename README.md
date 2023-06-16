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

- [ ] Re-write the bot in a more mainstream framework (i.e discord.py).
- [ ] Find a better hosting solution for Fall 2023. 
- [ ] Write a fix for discord's rate limiting being triggered. 

## Long Term
My aim is to have this bot up and running before the Fall 2023 semester so it can be used by students again. Once the re-write is complete, we will focus more on adding functionality and features. The bot is in a beta stage right now.

## Contributing
Welcome to the canvas discord bot project! This is a bot that can interact with the canvas API and do a lot of neat things! Here are some ways you can help us improve this project:

- **Suggest new features or commands.** If you have an idea for a cool or useful feature or command that the bot can do with images, please open an issue and let us know. We are always looking for new ways to make the bot more fun and creative.
- **Submit a pull request.** If you have written some code that adds or improves a feature or command, or you have fixed a bug or error, please submit a pull request with your changes. Make sure to follow the coding style and conventions of this project, and include a clear description of what you have done and why.
- **Review and test existing code.** If you want to help ensure the quality and functionality of the bot, you can review and test the existing code and provide feedback or suggestions. You can also report any issues or errors you encounter while using the bot.
- **Help us convert the bot to another library/framework.** We are currently using pycord (an experimental version) as the library for interacting with discord, but we are considering switching to another library/framework that might offer more features or stability, such as **discord.py**. If you have experience or knowledge in this area, 
