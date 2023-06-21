
<head>
    <link rel="stylesheet" href="styles.css">
</head><h1>Client</h1>
<p><span class="h4" id="Client">
    <span class="class">
        class 
    </span>
    Client
</span>
<br>
This repersents the Client you can use to interact with kick.<br>
<br>
<span class="h4">Parameters</span><br>
**options: Any<br>
<span style="margin-left: 30px">    Options that can be passed</span><br>
<br>
<span class="h4">Options</span><br>
whitelisted: bool = False<br>
<span style="margin-left: 30px">    If you have been api whitelisted. If set to True, the bypass script will not be used.</span><br>
bypass_port: int = 9090<br>
<span style="margin-left: 30px">    The port the bypass script is running on. Defaults to 9090</span><br>
<br>
<span class="h4">Attributes</span><br>
user: ClientUser | None<br>
<span style="margin-left: 30px">    The user you are logged in as. It is <a href="#None" class="hidden"><code>None</code></a> until <a href="#Client.login" class="hidden"><code>Client.login</code></a> is called.</span><br></p>
<h2>Methods</h2>
<p><span class="h4" id="Client.fetch_user">
    <span class="async">
        async def 
    </span>
    Client.fetch_user
</span>
<br>
Fetches a user from the API.<br>
<br>
<span class="h4">Parameters</span><br>
name: str<br>
<span style="margin-left: 30px">    The user's slug or username</span><br>
<br>
<span class="h4">Raises</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Fetching Failed</span><br>
NotFound<br>
<span style="margin-left: 30px">    No user with the username/slug exists</span><br>
<br>
<span class="h4">Returns</span><br>
User<br>
<span style="margin-left: 30px">    The user object associated with the streamer</span><br></p>
<p><span class="h4" id="Client.get_chatroom">
    <span class="def">
        def 
    </span>
    Client.get_chatroom
</span>
<br>
Gets a chatroom out of a cache that contains chatrooms that you are connected to.<br>
<br>
<span class="h4">Parameters</span><br>
chatroom_id: int<br>
<span style="margin-left: 30px">    The chatroom's id</span><br>
<br>
<span class="h4">Returns</span><br>
Chatroom | None<br>
<span style="margin-left: 30px">    Either the chatroom, or None</span><br></p>
<p><span class="h4" id="Client.event">
    <span class="at">
        @
    </span>
    Client.event
</span>
<br>
Lets you set an event outside of a subclass.<br></p>
<p><span class="h4" id="Client.login">
    <span class="async">
        async def 
    </span>
    Client.login
</span>
<br>
Authenticates yourself, and fills <a href="#Client.user" class="hidden"><a href="#Client.user" class="hidden"><code>Client.user</code></a></a><br>
Unlike <a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden"><code>Client.start</code></a></a></a>, this does not start the websocket<br>
<br>
<span class="h4">Parameters</span><br>
credentials: Credentials<br>
<span style="margin-left: 30px">    The credentials to authenticate yourself with</span><br></p>
<p><span class="h4" id="Client.start">
    <span class="async">
        async def 
    </span>
    Client.start
</span>
<br>
Starts the websocket so you can receive events<br>
And authenticate yourself if credentials are provided.<br>
<br>
<span class="h4">Parameters</span><br>
credentials: Optional[Credentials]<br>
<span style="margin-left: 30px">    The credentials to authenticate yourself with, if any</span><br></p>
<p><span class="h4" id="Client.login">
    <span class="async">
        async def 
    </span>
    Client.login
</span>
<br>
Authenticates yourself, and fills <a href="#Client.user" class="hidden"><a href="#Client.user" class="hidden"><code>Client.user</code></a></a><br>
Unlike <a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden"><code>Client.start</code></a></a></a>, this does not start the websocket<br>
<br>
<span class="h4">Parameters</span><br>
credentials: Credentials<br>
<span style="margin-left: 30px">    The credentials to authenticate yourself with</span><br></p>
<p><span class="h4" id="Client.run">
    <span class="def">
        def 
    </span>
    Client.run
</span>
<br>
Starts the websocket so you can receive events<br>
And authenticate yourself if credentials are provided.<br>
<br>
<a href="#Client.run" class="hidden"><code>Client.run</code></a> automatically calls <a href="#utils.setup_logging" class="hidden"><code>utils.setup_logging</code></a> with the provided kwargs, and calls <a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden"><code>Client.start</code></a></a></a>.<br>
<br>
<span class="h4">Parameters</span><br>
credentials: Optional[Credentials]<br>
<span style="margin-left: 30px">    The credentials to authenticate yourself with, if any</span><br></p>
<p><span class="h4" id="Client.close">
    <span class="async">
        async def 
    </span>
    Client.close
</span>
<br>
Closes the HTTPClient, no requests can be made after this.<br></p>
<p><span class="h4" id="Client.on_ready">
    <span class="async">
        async def 
    </span>
    Client.on_ready
</span>
<br>
on_ready is an event that can be overriden with the <a href="#Client.event" class="hidden"><a href="#Client.event" class="hidden"><code>Client.event</code></a></a> decorator or with a subclass.<br>
This is called after the client has started the websocket and is receiving events.<br></p>
<p><span class="h4" id="Client.on_message">
    <span class="async">
        async def 
    </span>
    Client.on_message
</span>
<br>
on_ready is an event that can be overriden with the <a href="#Client.event" class="hidden"><a href="#Client.event" class="hidden"><code>Client.event</code></a></a> decorator or with a subclass.<br>
This is called when a message is received over the websocket<br>
<br>
<span class="h4">Parameters</span><br>
message: Message<br>
<span style="margin-left: 30px">    The message that was received</span><br></p>
<hr>

<p><span class="h4" id="Credentials">
    <span class="class">
        class 
    </span>
    Credentials
</span>
<br>
This holds credentials that can be used to authenticate yourself with kick.<br>
<br>
<span class="h4">Parameters</span><br>
username: Optional[str]<br>
<span style="margin-left: 30px">    The username to login with. Can not be used with the <a href="#email" class="hidden"><a href="#email" class="hidden"><code>email</code></a></a> arg</span><br>
email: Optional[str]<br>
<span style="margin-left: 30px">    The email to login with. Can not be used with the <a href="#username" class="hidden"><a href="#username" class="hidden"><code>username</code></a></a> arg</span><br>
password: str<br>
<span style="margin-left: 30px">    The account's password</span><br>
one_time_password: Optional[str]<br>
<span style="margin-left: 30px">    The 2FA code to login with</span><br>
<br>
<span class="h4">Attributes</span><br>
username: Optional[str]<br>
<span style="margin-left: 30px">    The username to login with. Can not be used with the <a href="#email" class="hidden"><a href="#email" class="hidden"><code>email</code></a></a> arg</span><br>
email: Optional[str]<br>
<span style="margin-left: 30px">    The email to login with. Can not be used with the <a href="#username" class="hidden"><a href="#username" class="hidden"><code>username</code></a></a> arg</span><br>
password: str<br>
<span style="margin-left: 30px">    The account's password</span><br>
one_time_password: Optional[str]<br>
<span style="margin-left: 30px">    The 2FA code to login with</span><br></p>
<h1>Asset</h1>
<hr>

<p><span class="h4" id="Asset">
    <span class="class">
        class 
    </span>
    Asset
</span>
<br>
A class which repersents a kick asset.<br></p>
<h2>Methods</h2>
<p><span class="h4" id="Asset.read">
    <span class="async">
        async def 
    </span>
    Asset.read
</span>
<br>
Fetches the asset from kick<br>
<br>
<span class="h4">Raises</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Fetching the asset failed</span><br>
NotFound<br>
<span style="margin-left: 30px">    Asset no longer exists</span><br>
<br>
<span class="h4">Returns</span><br>
bytes<br>
<span style="margin-left: 30px">    The asset's bytes</span><br></p>
<p><span class="h4" id="Asset.save">
    <span class="async">
        async def 
    </span>
    Asset.save
</span>
<br>
Saves the asset into a file-like object<br>
<br>
<span class="h4">Parameters</span><br>
fp: str | bytes | os.PathLike[Any] | BufferedIOBase<br>
<span style="margin-left: 30px">    The file-like object for the asset to be written to.</span><br>
<span style="margin-left: 30px">    If a filepath is given, then a file will be created instead.</span><br>
seek_begin: bool<br>
<span style="margin-left: 30px">    Whether to seek to the beginning of the file after saving is</span><br>
<span style="margin-left: 30px">    successfully done.</span><br>
<br>
<span class="h4">Raises</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Fetching the asset failed</span><br>
NotFound<br>
<span style="margin-left: 30px">    Asset no longer exists</span><br>
<br>
<span class="h4">Returns</span><br>
int<br>
<span style="margin-left: 30px">    The amount of bytes written</span><br></p>
<h1>Badges</h1>
<hr>

<p>{{ChatBadge}}
[[ChatBadge]]</p>
<hr>

<p>{{SubscriberBadge}}
[[SubscriberBadge]]</p>
<h1>Categories</h1>
<p>{{ParentCategory}}
[[ParentCategory]]</p>
<hr>

<p>{{Category}}
[[Category]]</p>
<h1>Chatroom</h1>
<p><span class="h4" id="Chatroom">
    <span class="class">
        class 
    </span>
    Chatroom
</span></p>
<h2>Methods</h2>
<p><span class="h4" id="Chatroom.connect">
    <span class="async">
        async def 
    </span>
    Chatroom.connect
</span>
<br>
Connects to the chatroom, making it so you can now listen for the messages.<br></p>
<p><span class="h4" id="Chatroom.disconnect">
    <span class="async">
        async def 
    </span>
    Chatroom.disconnect
</span>
<br>
disconnects to the chatroom, making it so you can no longer listen for the messages.<br></p>
<p><span class="h4" id="Chatroom.send">
    <span class="async">
        async def 
    </span>
    Chatroom.send
</span>
<br>
Sends a message in the chatroom<br>
<br>
<span class="h4">Parameters</span><br>
content: str<br>
<span style="margin-left: 30px">    The message's content</span><br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    Streamer or chatter not found</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Sending the message failed</span><br>
Forbidden<br>
<span style="margin-left: 30px">    You are unauthorized from sending the message</span><br></p>
<p><span class="h4" id="Chatroom.fetch_chatter">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_chatter
</span>
<br>
Fetches a chatroom's chatter<br>
<br>
<span class="h4">Parameters</span><br>
chatter_name: str<br>
<span style="margin-left: 30px">    The chatter's username</span><br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    Streamer or chatter not found</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Fetching the chatter failed</span><br>
<br>
<span class="h4">Returns</span><br>
Chatter<br>
<span style="margin-left: 30px">    The chatter</span><br></p>
<p><span class="h4" id="Chatroom.fetch_bans">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_bans
</span>
<br>
Fetches the chatroom's bans<br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    Streamer Not Found</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Fetching the bans failed</span><br>
<br>
<span class="h4">Returns</span><br>
AsyncIterator[BanEntry]<br>
<span style="margin-left: 30px">    Yields all of the ban entries</span><br></p>
<p><span class="h4" id="Chatroom.fetch_banned_words">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_banned_words
</span>
<br>
Fetches the chatroom's banned words<br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    Streamer Not Found</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Fetching the words failed</span><br>
<br>
<span class="h4">Returns</span><br>
list[str]<br>
<span style="margin-left: 30px">    A list of the banned words</span><br></p>
<p><span class="h4" id="Chatroom.fetch_rules">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_rules
</span>
<br>
Fetches the chatroom's rules<br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    Streamer Not Found</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Fetching the rules failed</span><br>
<br>
<span class="h4">Returns</span><br>
str<br>
<span style="margin-left: 30px">    The rules</span><br></p>
<p><span class="h4" id="Chatroom.fetch_poll">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_poll
</span>
<br>
Gets a poll from the chatroom<br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    There is no poll in the current chatroom or Streamer Not Found</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Fetching the poll failed</span><br>
<br>
<span class="h4">Returns</span><br>
Poll<br>
<span style="margin-left: 30px">    The poll</span><br></p>
<p><span class="h4" id="Chatroom.fetch_emotes">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_emotes
</span>
<br>
Fetches the emotes from the current chatroom.<br>
<br>
<span class="h4">Parameters</span><br>
include_global: bool = False<br>
<span style="margin-left: 30px">    Wether to include global emotes or not</span><br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    Streamer Not Found</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Fetching the bans failed</span><br>
<br>
<span class="h4">Returns</span><br>
AsyncIterator[Emote]<br>
<span style="margin-left: 30px">    Yields each emote. Starting with from the chatroom, then global</span><br></p>
<h1>BanEntry</h1>
<p><span class="h4" id="BanEntry">
    <span class="class">
        class 
    </span>
    BanEntry
</span></p>
<h2>Methods</h2>
<p><span class="h4" id="BanEntry.unban">
    <span class="async">
        async def 
    </span>
    BanEntry.unban
</span>
<br>
Unbans the chatter from the chatroom.<br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    Streamer or chatter not found</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Unbanning the chatter failed</span><br>
Forbidden<br>
<span style="margin-left: 30px">    You are unauthorized from unbanning the chatter</span><br></p>
<h1>Users</h1>
<p><span class="h4" id="User">
    <span class="class">
        class 
    </span>
    User
</span></p>
<h2>Methods</h2>
<p><span class="h4" id="User.fetch_videos">
    <span class="def">
        def 
    </span>
    User.fetch_videos
</span></p>
<p><span class="h4" id="User.fetch_gift_leaderboard">
    <span class="def">
        def 
    </span>
    User.fetch_gift_leaderboard
</span></p>
<hr>

<p><span class="h4" id="PartialUser">
    <span class="class">
        class 
    </span>
    PartialUser
</span></p>
<hr>

<p><span class="h4" id="ClientUser">
    <span class="class">
        class 
    </span>
    ClientUser
</span></p>
<h2>Methods</h2>
<p><span class="h4" id="ClientUser.fetch_videos">
    <span class="def">
        def 
    </span>
    ClientUser.fetch_videos
</span></p>
<hr>

<p>{{Chatter}}
[[Chatter]]</p>
<hr>

<p><span class="h4" id="Author">
    <span class="class">
        class 
    </span>
    Author
</span></p>
<h1>Messages</h1>
<p><span class="h4" id="Message">
    <span class="class">
        class 
    </span>
    Message
</span></p>
<hr>

<p><span class="h4" id="PartialMessage">
    <span class="class">
        class 
    </span>
    PartialMessage
</span></p>
<h1>Emote</h1>
<p><span class="h4" id="Emote">
    <span class="class">
        class 
    </span>
    Emote
</span></p>
<h1>Enums</h1>
<p><span class="h4" id="ChatroomChatMode">
    <span class="class">
        class 
    </span>
    ChatroomChatMode
</span></p>
<h1>Leaderboard</h1>
<p><span class="h4" id="GiftLeaderboardEntry">
    <span class="class">
        class 
    </span>
    GiftLeaderboardEntry
</span></p>
<hr>

<p><span class="h4" id="GiftLeaderboard">
    <span class="class">
        class 
    </span>
    GiftLeaderboard
</span></p>
<h1>Livestream</h1>
<p><span class="h4" id="Livestream">
    <span class="class">
        class 
    </span>
    Livestream
</span></p>
<h1>Polls</h1>
<p>{{PollOption}}
[[PollOption]]</p>
<h2>Methods</h2>
<p>{{PollOption.vote}}
[[PollOption.vote]]</p>
<hr>

<p>{{Poll}}
[[Poll]]</p>
<h2>Methods</h2>
<p>{{Poll.delete}}
[[Poll.delete]]</p>
<h1>Videos</h1>
<p><span class="h4" id="Video">
    <span class="class">
        class 
    </span>
    Video
</span></p>
<h1>Other</h1>
<p><span class="h4" id="Socials">
    <span class="class">
        class 
    </span>
    Socials
</span></p>
<h1>Errors</h1>
<p><span class="h4" id="CloudflareBypassException">
    <span class="class">
        class 
    </span>
    CloudflareBypassException
</span></p>
<hr>

<p><span class="h4" id="KickException">
    <span class="class">
        class 
    </span>
    KickException
</span></p>
<hr>

<p><span class="h4" id="LoginFailure">
    <span class="class">
        class 
    </span>
    LoginFailure
</span></p>
<hr>

<p><span class="h4" id="HTTPException">
    <span class="class">
        class 
    </span>
    HTTPException
</span></p>
<hr>

<p><span class="h4" id="Forbidden">
    <span class="class">
        class 
    </span>
    Forbidden
</span></p>
<hr>

<p><span class="h4" id="NotFound">
    <span class="class">
        class 
    </span>
    NotFound
</span></p>
<hr>

<p><span class="h4" id="InternalKickException">
    <span class="class">
        class 
    </span>
    InternalKickException
</span></p>