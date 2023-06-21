
<head>
    <link rel="stylesheet" href="styles.css">
</head><h1>Kick.py</h1>
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
<p><a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><code>&lt;/a&gt;&lt;/a&gt;&lt;/a&gt;&lt;/a&gt;`bash
pip install git+https://github.com/cibere/kick.py
&lt;a href="#" class="hidden"&gt;&lt;a href="#" class="hidden"&gt;&lt;a href="#" class="hidden"&gt;&lt;a href="#" class="hidden"&gt;</code></a></a></a></a>`</p>
<p>If you are api whitelisted (meaning you are whitelisted from cloudflare), then you can pass <a href="#whitelisted=True" class="hidden"><code>whitelisted=True</code></a> to your <a href="#Client" class="hidden"><a href="#Client" class="hidden"><code>Client</code></a></a> constructor. Otherwise you should setup the bypass script.</p>
<h2>Setting up the bypass script</h2>
<p><em>these steps assume your python executable is <a href="#python" class="hidden"><code>python</code></a>, but that might not be the case</em></p>
<ol>
<li>Install <a href="https://go.dev/doc/install">golang</a></li>
<li>Run <a href="#python -m kick bypass create --port 9090 --fp bypass.go" class="hidden"><code>python -m kick bypass create --port 9090 --fp bypass.go</code></a> to create the script.</li>
<li>To install the dependencies run <a href="#python -m kick bypass install" class="hidden"><code>python -m kick bypass install</code></a></li>
<li>To start the script run <a href="#go run bypass.go" class="hidden"><code>go run bypass.go</code></a></li>
</ol>
<p>If you set a port other than <a href="#9090" class="hidden"><code>9090</code></a> for the bypass script, make sure to pass <a href="#bypass_port=THE_PORT" class="hidden"><code>bypass_port=THE_PORT</code></a> into your <a href="#Client" class="hidden"><a href="#Client" class="hidden"><code>Client</code></a></a> constructor.</p>
<h2>Basic Example</h2>
<p><a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><code>`&lt;/a&gt;&lt;/a&gt;&lt;/a&gt;&lt;/a&gt;</code>py
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
<a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><a href="#" class="hidden"><code>`&lt;/a&gt;&lt;/a&gt;&lt;/a&gt;&lt;/a&gt;</code></p>