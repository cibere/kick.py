
<head>
    <link rel="stylesheet" href="style.css">
</head>
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

> ! **This project is still in early alpha, so it might not work as expected but here is how installation goes.**

Install from github _requires [git](https://git-scm.com/) to be installed_

<a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden">``</a></a></a></a>`bash
pip install git+https://github.com/cibere/kick.py
<a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden">``</a></a></a></a>`

If you are api whitelisted (meaning you are whitelisted from cloudflare), then you can pass <a href="#whitelisted=True" class="hidden">`whitelisted=True`</a> to your <a href="#Client" class="hidden"><a href="#Client" class="hidden">`Client`</a></a> constructor. Otherwise you should setup the bypass script.

## Setting up the bypass script

_these steps assume your python executable is <a href="#python" class="hidden">`python`</a>, but that might not be the case_

1. Install [golang](https://go.dev/doc/install)
2. Run <a href="#python -m kick bypass create" class="hidden">`python -m kick bypass create`</a> to create the script. See <a href="#python -m kick bypass create --help" class="hidden">`python -m kick bypass create --help`</a> for information about running the command.
   > Options include: proxy, port, filepath
3. To install the dependencies run <a href="#python -m kick bypass install" class="hidden">`python -m kick bypass install`</a>.
4. To start the script run <a href="#go run bypass.go" class="hidden">`go run bypass.go`</a>.

If you set a port other than <a href="#9090" class="hidden">`9090`</a> for the bypass script, make sure to pass <a href="#bypass_port=THE_PORT" class="hidden">`bypass_port=THE_PORT`</a> into your <a href="#Client" class="hidden"><a href="#Client" class="hidden">`Client`</a></a> constructor.

## Basic Example

<a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden">``</a></a></a></a>`py
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
<a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden">``</a></a></a></a>`
