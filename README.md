# Setup

## First-time only

Make sure you have the latest version of python3 installed on your computer. Before doing any development:
1. Run `python3 -m venv venv/`
2. Run `source venv/bin/activate`
3. Run `pip install -r requirements.txt`
4. Create a file in the root directory called `.env` and add the following string to it: `DISCORD_TOKEN={discord api token}`, where `{discord api token}` should be replaced by the token provided in the server-development channel in the pinned message.
5. Install MongoDB for your platform using the instructions at https://www.mongodb.com/docs/manual/administration/install-community/.
6. On the Discord server, ensure that there is a `Carpool Admin` role assigned to every user who should have the permissions to invoke carpool bot admin commands (these are all the commands with the `-admin` suffix). This role should also be assigned to the bot itself.
7. Create an `Inactive` Discord server role for server members who will not be participating in the team for a given term.
8. Create three channels:
    1. `#carpool-scheduling` should be open to everyone, and will be the place where regular users can type their commands to the bot.
    2. `#carpool-admin` should be open to those with the `Carpool Admin` role, and will be the place where Carpool Admins can send their admin commands privately.
    3. `#carpool-official` should be open to everyone, and will be where the bot posts the carpools. It may be useful to restrict posting in this channel to only `Carpool Admin`s.
9. Create a new database entry for yourself by running the discord command `!temp-reg-user` in any channel the Carpool Bot is a part of. You only need to do this once.

## All other times

Before doing any development:
1. Run `source venv/bin/activate`
2. Run the bot with the command `python3 src/main.py` and wait for a console message saying the bot has connected to discord.