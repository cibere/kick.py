# Kick.py

Kick.py _will_ be an async api wrapper for [kick.com](https://kick.com) once the api is public, and is documented. Though once its there, I will gladly accept help in making this :D

## Table Of Contents

- [API Reference](/api_reference)
- [Features](#features)
- [Installation](#installation)
- [Setting up the bypass script](#setting-up-the-bypass-script)
- [Basic Example](#basic-example)

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

> !**This project is still in early alpha, so it might not work as expected but here is how installation goes.**

Install from github _requires [git](https://git-scm.com/) to be installed_

```bash
pip install git+https://github.com/cibere/kick.py
```

If you are api whitelisted (meaning you are whitelisted from cloudflare), then you can pass `whitelisted=True` to your `Client` constructor. Otherwise you should setup the bypass script.

## Setting up the bypass script

_these steps assume your python executable is `python`, but that might not be the case_

1. Install [golang](https://go.dev/doc/install)
2. Run `python -m kick bypass create --port 9090 --fp bypass.go` to create the script.
3. If you require proxy support edit `bypass.go`and uncomment `// Proxy: "http://username:password@hostname.com:port",`.
4. To install the dependencies run `python -m kick bypass install`.
5. To start the script run `go run bypass.go`.

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
