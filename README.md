# Kick.py

<a href="https://discord.gg/AGuwPB2XfV"><img src="https://discord.com/api/guilds/1046574190242828349/embed.png" alt="Discord Server Invite"></a>

Kick.py _will_ be an async api wrapper for [kick.com](https://kick.com) once the api is public, and is documented. Though once its there, I will gladly accept help in making this :D

## Documentation
Our docs are being hosted on https://kickpy.cibere.dev

## Features

- Emotes (Global and per streamer)
- Videos
- Livestreams
- Users
- Chatters
- Reading Messages
- Sending Messages
- Cloudflare Bypass
- Assets
- Full Ban Support
- Leaderboards
- Regenerate Token on expiration
- Proxy Support

## Installation

> ! **This project is still in early alpha, so it might not work as expected but here is how installation goes.**

Install from github _requires [git](https://git-scm.com/) to be installed_

```bash
pip install git+https://github.com/cibere/kick.py
```

If you are api whitelisted (meaning you are whitelisted from cloudflare), then you can pass `whitelisted=True` to your `Client` constructor. Otherwise you should setup the bypass script.

## Setting up the bypass script

_these steps assume your python executable is `python`, but that might not be the case_

1. Install [golang](https://go.dev/doc/install)
2. Run `python -m kick bypass create` to create the script. See `python -m kick bypass create --help` for information about running the command.
   > Options include: proxy, port, filepath
3. To install the dependencies run `python -m kick bypass install`.
4. To start the script run `go run bypass.go`.

If you set a port other than `9090` for the bypass script, make sure to pass `bypass_port=THE_PORT` into your `Client` constructor.

## Basic Example

```py
import kick
import asyncio

client = kick.Client()

@client.event
async def on_message(message):
    print(f"Received message from {message.author.username}")

@client.event
async def on_ready():
    print("I'm Ready!")

    user = await client.fetch_user("xQc")
    await user.chatroom.connect()


client.run()
```
