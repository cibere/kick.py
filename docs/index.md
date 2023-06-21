
<head>
    <link rel="stylesheet" href="styles.css">
</head><p>!IGNORE-FORMAT</p>
<h1>Kick.py</h1>
<p>Kick.py <em>will</em> be an async api wrapper for <a href="https://kick.com">kick.com</a> once the api is public, and is documented. Though once its there, I will gladly accept help in making this :D</p>
<h2>Table Of Contents</h2>
<ul>
<li><a href="/api_reference">API Reference</a></li>
<li><a href="#features">Features</a></li>
<li><a href="#installation">Installation</a></li>
<li><a href="#setting-up-the-bypass-script">Setting up the bypass script</a></li>
<li><a href="#basic-example">Basic Example</a></li>
</ul>
<h2>Features</h2>
<ul>
<li>Emotes (Global and per streamer)</li>
<li>Videos</li>
<li>Livestreams</li>
<li>Users</li>
<li>Chatters</li>
<li>Reading Messages</li>
<li>Sending Messages</li>
<li>Cloudflare Bypass</li>
<li>Assets</li>
<li>Full Ban Support</li>
<li>Leaderboards</li>
<li>Regenerate Token on expiration</li>
</ul>
<h2>Installation</h2>
<blockquote>
<p>!<strong>This project is still in early alpha, so it might not work as expected but here is how installation goes.</strong></p>
</blockquote>
<p>Install from github *requires <a href="https://git-scm.com/">git</a> to be installed*</p>
<p><code>bash
pip install git+https://github.com/cibere/kick.py</code></p>
<p>If you are api whitelisted (meaning you are whitelisted from cloudflare), then you can pass <code>whitelisted=True</code> to your <code>Client</code> constructor. Otherwise you should setup the bypass script.</p>
<h2>Setting up the bypass script</h2>
<p><em>these steps assume your python executable is <code>python</code>, but that might not be the case</em></p>
<ol>
<li>Install <a href="https://go.dev/doc/install">golang</a></li>
<li>Run <code>python -m kick bypass create --port 9090 --fp bypass.go</code> to create the script.</li>
<li>To install the dependencies run <code>python -m kick bypass install</code></li>
<li>To start the script run <code>go run bypass.go</code></li>
</ol>
<p>If you set a port other than <code>9090</code> for the bypass script, make sure to pass <code>bypass_port=THE_PORT</code> into your <code>Client</code> constructor.</p>
<h2>Basic Example</h2>
<p>```py
import kick
import asyncio</p>
<p>client = kick.Client()</p>
<p>@client.event
async def on_message(message):
    print(f"Received message from {message.author.username}")</p>
<p>@client.event
async def on_ready():
    print("I'm Ready!")</p>
<pre><code>user = await client.fetch_user("xQc")
await user.chatroom.connect()
</code></pre>
<p>client.run()
```</p>