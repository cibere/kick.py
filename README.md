# kick.py

Kick.py _will_ be an async api wrapper for [kick.com](https://kick.com) once the api is public, and is documented. Though once its there, I will gladly accept help in making this :D

# Features

- Emotes (Global and per streamer)
- Videos
- Livestreams
- Users
- Chatters
- Reading Messages
- Sending Messages
- Cloudflare Bypass
- Assets

# Installation

> !**This project is still in early alpha, so it might not work as expected but here is how installation goes.**

Install from github \*requires [git](https://git-scm.com/) to be installed\*

```bash
pip install git+https://github.com/cibere/kick.py
```

If you are api whitelisted (meaning you are whitelisted from cloudflare), then you can pass `whitelisted=True` to your `Client` constructor. Otherwise you should setup the bypass script.

## Setting up the bypass script

_these steps assume your python executable is `python`, but that might not be the case_

1. Install [golang](https://go.dev/doc/install)
2. Run `python -m kick bypass create --port 9090 --fp bypass.go` to create the script.
3. To install the dependencies run `python -m kick bypass install`
4. To start the script run `go run bypass.go`

If you set a port other than `9090` for the bypass script, make sure to pass `bypass_port=THE_PORT` into your `Client` constructor.

# Basic Example

```py
import kick
import asyncio

client = kick.Client()

@client.event
async def on_ready():
    print("I'm Ready!")

async def main():
    credentials = kick.Credentials(
        username = ...,
        password = ...
    )
    await client.start(credentials)

asyncio.run(main())
```

# TODO

- ratelimit handling (ratelimit is unknown on how it works)
- cache (idk how I will do this)
- see types folder for things that still need a payload, and perhaps a dataclass.
- Add partials
- Proper handling of `User.playback_url`

# FAQ

> Q: Why does this package exist even though the api is not public yet?
>
> A: Because I'm too impatient, and want to start making the wrapper now
