# CryptoBot

A Discord bot to get general information and notifications about crypto tokens

Bot ID: 1041934826195927130

## How to run the bot

Pre-requisites
> Python3.6 >=

Get your own application with Bot Token from here https://discord.com/developers/applications/

add to `auth/cryptobot.json`

`{"token": "bot-token-here"}`

### Configure virtual environment

`python3 -m venv venv` # Install virtual environment named `venv`

`source ./venv/bin/activate` # activate virtal env in Linux

`./venv/bin/activate.ps1` # activate virtal env in Windows

### Install packages with pip

`python3 -m pip install --upgrade pip` # upgrade pip

`python3 -m pip install -r requirements.txt` # install list of packages from file

### Run

`python3 bot.py`


# Bot Standard Permissions

Bot permissions: (Text Permissions)
Send Messages
Attach Files
Read Message History
Add Reactions
Use Slash Commands

Bot permissions integer:
2147584064

Add bot URL:
https://discord.com/api/oauth2/authorize?client_id=1041934826195927130&permissions=2147584064&scope=bot
