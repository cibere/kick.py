
<head>
    <link rel="stylesheet" href="style.css">
</head>
# Client


<a href="#Client" class="hidden" class="h4" id="Client">
    <span class="class">
        class 
    </span>
    Client
</a>

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
<span style="margin-left: 30px">    The user you are logged in as. It is <a href="#None" class="hidden">`None`</a> until <a href="#Client.login" class="hidden">`Client.login`</a> is called.</span><br>

## Methods


<a href="#Client.fetch_user" class="hidden" class="h4" id="Client.fetch_user">
    <span class="async">
        async def 
    </span>
    Client.fetch_user
</a>

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
<span style="margin-left: 30px">    The user object associated with the streamer</span><br>


<a href="#Client.get_chatroom" class="hidden" class="h4" id="Client.get_chatroom">
    <span class="def">
        def 
    </span>
    Client.get_chatroom
</a>

<br>
Gets a chatroom out of a cache that contains chatrooms that you are connected to.<br>
<br>
<span class="h4">Parameters</span><br>
chatroom_id: int<br>
<span style="margin-left: 30px">    The chatroom's id</span><br>
<br>
<span class="h4">Returns</span><br>
Chatroom | None<br>
<span style="margin-left: 30px">    Either the chatroom, or None</span><br>


<a href="#Client.get_partial_chatter" class="hidden" class="h4" id="Client.get_partial_chatter">
    <span class="def">
        def 
    </span>
    Client.get_partial_chatter
</a>

<br>
Gets a partial chatter instance by the streamer and chatter names provided.<br>
<br>
<span class="h4">Parameters</span><br>
streamer_name: str<br>
<span style="margin-left: 30px">    The streamer's username or slug</span><br>
chatter_name: str<br>
<span style="margin-left: 30px">    The chatter's username or slug</span><br>
<br>
<span class="h4">Returns</span><br>
<a href="#PartialChatter" class="hidden">`PartialChatter`</a><br>
<span style="margin-left: 30px">    The partial chatter</span><br>


<a href="#Client.get_partial_user" class="hidden" class="h4" id="Client.get_partial_user">
    <span class="def">
        def 
    </span>
    Client.get_partial_user
</a>

<br>
Gets a partial user instance by the username and id provided.<br>
<br>
<span class="h4">Parameters</span><br>
username: str<br>
<span style="margin-left: 30px">    The user's name</span><br>
id: int<br>
<span style="margin-left: 30px">    The user's id</span><br>
<br>
<span class="h4">Returns</span><br>
<a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden">`PartialUser`</a></a></a></a><br>
<span style="margin-left: 30px">    The partial user</span><br>


<a href="#Client.event" class="hidden" class="h4" id="Client.event">
    <span class="at">
        @
    </span>
    Client.event
</a>

<br>
Lets you set an event outside of a subclass.<br>


<a href="#Client.login" class="hidden" class="h4" id="Client.login">
    <span class="async">
        async def 
    </span>
    Client.login
</a>

<br>
Authenticates yourself, and fills <a href="#Client.user" class="hidden"><a href="#Client.user" class="hidden">`Client.user`</a></a><br>
Unlike <a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden">`Client.start`</a></a></a>, this does not start the websocket<br>
<br>
<span class="h4">Parameters</span><br>
credentials: Credentials<br>
<span style="margin-left: 30px">    The credentials to authenticate yourself with</span><br>


<a href="#Client.start" class="hidden" class="h4" id="Client.start">
    <span class="async">
        async def 
    </span>
    Client.start
</a>

<br>
Starts the websocket so you can receive events<br>
And authenticate yourself if credentials are provided.<br>
<br>
<span class="h4">Parameters</span><br>
credentials: Optional[Credentials]<br>
<span style="margin-left: 30px">    The credentials to authenticate yourself with, if any</span><br>


<a href="#Client.login" class="hidden" class="h4" id="Client.login">
    <span class="async">
        async def 
    </span>
    Client.login
</a>

<br>
Authenticates yourself, and fills <a href="#Client.user" class="hidden"><a href="#Client.user" class="hidden">`Client.user`</a></a><br>
Unlike <a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden">`Client.start`</a></a></a>, this does not start the websocket<br>
<br>
<span class="h4">Parameters</span><br>
credentials: Credentials<br>
<span style="margin-left: 30px">    The credentials to authenticate yourself with</span><br>


<a href="#Client.run" class="hidden" class="h4" id="Client.run">
    <span class="def">
        def 
    </span>
    Client.run
</a>

<br>
Starts the websocket so you can receive events<br>
And authenticate yourself if credentials are provided.<br>
<br>
<a href="#Client.run" class="hidden">`Client.run`</a> automatically calls <a href="#utils.setup_logging" class="hidden">`utils.setup_logging`</a> with the provided kwargs, and calls <a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden"><a href="#Client.start" class="hidden">`Client.start`</a></a></a>.<br>
<br>
<span class="h4">Parameters</span><br>
credentials: Optional[Credentials]<br>
<span style="margin-left: 30px">    The credentials to authenticate yourself with, if any</span><br>


<a href="#Client.close" class="hidden" class="h4" id="Client.close">
    <span class="async">
        async def 
    </span>
    Client.close
</a>

<br>
Closes the HTTPClient, no requests can be made after this.<br>


<a href="#Client.on_ready" class="hidden" class="h4" id="Client.on_ready">
    <span class="async">
        async def 
    </span>
    Client.on_ready
</a>

<br>
on_ready is an event that can be overriden with the <a href="#Client.event" class="hidden"><a href="#Client.event" class="hidden">`Client.event`</a></a> decorator or with a subclass.<br>
This is called after the client has started the websocket and is receiving events.<br>


<a href="#Client.on_message" class="hidden" class="h4" id="Client.on_message">
    <span class="async">
        async def 
    </span>
    Client.on_message
</a>

<br>
on_ready is an event that can be overriden with the <a href="#Client.event" class="hidden"><a href="#Client.event" class="hidden">`Client.event`</a></a> decorator or with a subclass.<br>
This is called when a message is received over the websocket<br>
<br>
<span class="h4">Parameters</span><br>
message: Message<br>
<span style="margin-left: 30px">    The message that was received</span><br>

<hr>


<a href="#Credentials" class="hidden" class="h4" id="Credentials">
    <span class="class">
        class 
    </span>
    Credentials
</a>

<br>
This holds credentials that can be used to authenticate yourself with kick.<br>
<br>
<span class="h4">Parameters</span><br>
username: Optional[str]<br>
<span style="margin-left: 30px">    The username to login with. Can not be used with the <a href="#email" class="hidden"><a href="#email" class="hidden">`email`</a></a> arg</span><br>
email: Optional[str]<br>
<span style="margin-left: 30px">    The email to login with. Can not be used with the <a href="#username" class="hidden"><a href="#username" class="hidden">`username`</a></a> arg</span><br>
password: str<br>
<span style="margin-left: 30px">    The account's password</span><br>
one_time_password: Optional[str]<br>
<span style="margin-left: 30px">    The 2FA code to login with</span><br>
<br>
<span class="h4">Attributes</span><br>
username: Optional[str]<br>
<span style="margin-left: 30px">    The username to login with. Can not be used with the <a href="#email" class="hidden"><a href="#email" class="hidden">`email`</a></a> arg</span><br>
email: Optional[str]<br>
<span style="margin-left: 30px">    The email to login with. Can not be used with the <a href="#username" class="hidden"><a href="#username" class="hidden">`username`</a></a> arg</span><br>
password: str<br>
<span style="margin-left: 30px">    The account's password</span><br>
one_time_password: Optional[str]<br>
<span style="margin-left: 30px">    The 2FA code to login with</span><br>

# Asset

<hr>


<a href="#Asset" class="hidden" class="h4" id="Asset">
    <span class="class">
        class 
    </span>
    Asset
</a>

<br>
A class which repersents a kick asset.<br>
<br>
<span class="h4">Attributes</span><br>
url: str<br>
<span style="margin-left: 30px">    The asset's url</span><br>

## Methods


<a href="#Asset.read" class="hidden" class="h4" id="Asset.read">
    <span class="async">
        async def 
    </span>
    Asset.read
</a>

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
<span style="margin-left: 30px">    The asset's bytes</span><br>


<a href="#Asset.save" class="hidden" class="h4" id="Asset.save">
    <span class="async">
        async def 
    </span>
    Asset.save
</a>

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
<span style="margin-left: 30px">    The amount of bytes written</span><br>

# Badges

<hr>


<a href="#ChatBadge" class="hidden" class="h4" id="ChatBadge">
    <span class="class">
        class 
    </span>
    ChatBadge
</a>

<br>
A dataclass which represents a badge from a chatroon.<br>
<br>
<span class="h4">Attributes</span><br>
type: str<br>
<span style="margin-left: 30px">    The type of badge</span><br>
text: str<br>
<span style="margin-left: 30px">    The badge's text</span><br>
count: int<br>
<span style="margin-left: 30px">    How many of that badge they have</span><br>
active: bool<br>
<span style="margin-left: 30px">    If the chatter actively has the badge</span><br>

<hr>


<a href="#SubscriberBadge" class="hidden" class="h4" id="SubscriberBadge">
    <span class="class">
        class 
    </span>
    SubscriberBadge
</a>

<br>
A dataclass which represents a subscriber badge from a channel.<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    The badge's id</span><br>
channel_id: int<br>
<span style="margin-left: 30px">    The id of the channel the chatter is subscribed too</span><br>
months: int<br>
<span style="margin-left: 30px">    How many months they have been subscribed to the chatter</span><br>
image: <a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden">`Asset`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    The badge's image</span><br>

# Categories


<a href="#ParentCategory" class="hidden" class="h4" id="ParentCategory">
    <span class="class">
        class 
    </span>
    ParentCategory
</a>

<br>
A dataclass which represents one of kick's main categories<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    The categorie's ID</span><br>
name: str<br>
<span style="margin-left: 30px">    The categorie's name</span><br>
slug: str<br>
<span style="margin-left: 30px">    The categorie's slug</span><br>
icon: <a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden">`Asset`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    The categorie's icon</span><br>

<hr>


<a href="#Category" class="hidden" class="h4" id="Category">
    <span class="class">
        class 
    </span>
    Category
</a>

<br>
A dataclass which represents one of kick's sub categories<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    The categorie's ID?</span><br>
category_id: str<br>
<span style="margin-left: 30px">    The categorie's ID?</span><br>
slug: str<br>
<span style="margin-left: 30px">    The categorie's slug</span><br>
name: str<br>
<span style="margin-left: 30px">    The categorie's name</span><br>
tags: list[str]<br>
<span style="margin-left: 30px">    A list of the categorie's tags</span><br>
description: str | None<br>
<span style="margin-left: 30px">    The categorie's description, if any</span><br>
parent: <a href="#ParentCategory" class="hidden">`ParentCategory`</a><br>
<span style="margin-left: 30px">    The categorie's parent category.</span><br>

# Chatroom


<a href="#Chatroom" class="hidden" class="h4" id="Chatroom">
    <span class="class">
        class 
    </span>
    Chatroom
</a>

<br>
A dataclass that represents a kick chatroom.<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    The chatroom's id</span><br>
chatable_type: str<br>
<span style="margin-left: 30px">    The chatroom's type</span><br>
created_at: datetime.datetime<br>
<span style="margin-left: 30px">    When the chatroom was created</span><br>
updated_at: datetime.datetime<br>
<span style="margin-left: 30px">    When the chatroom was last updated</span><br>
chat_mode: ChatroomChatMode<br>
<span style="margin-left: 30px">    The mode the chatroom is in</span><br>
slowmode: bool<br>
<span style="margin-left: 30px">    Wether slowmode is enabled</span><br>
followers_mode: bool<br>
<span style="margin-left: 30px">    Wether followers_mode is enabled</span><br>
subscribers_mode: bool<br>
<span style="margin-left: 30px">    Wether subscribers_mode is enabled</span><br>
emotes_mode: bool<br>
<span style="margin-left: 30px">    Wether emotes_mode is enabled</span><br>
message_interval: int<br>
<span style="margin-left: 30px">    Unknown on what this is</span><br>
following_min_duration: int<br>
<span style="margin-left: 30px">    Unknown on what this is</span><br>
streamer: <a href="#User" class="hidden"><a href="#User" class="hidden"><a href="#User" class="hidden">`User`</a></a></a><br>
<span style="margin-left: 30px">    The user who this chatroom belongs to</span><br>

## Methods


<a href="#Chatroom.connect" class="hidden" class="h4" id="Chatroom.connect">
    <span class="async">
        async def 
    </span>
    Chatroom.connect
</a>

<br>
Connects to the chatroom, making it so you can now listen for the messages.<br>


<a href="#Chatroom.disconnect" class="hidden" class="h4" id="Chatroom.disconnect">
    <span class="async">
        async def 
    </span>
    Chatroom.disconnect
</a>

<br>
disconnects to the chatroom, making it so you can no longer listen for the messages.<br>


<a href="#Chatroom.send" class="hidden" class="h4" id="Chatroom.send">
    <span class="async">
        async def 
    </span>
    Chatroom.send
</a>

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
<span style="margin-left: 30px">    You are unauthorized from sending the message</span><br>


<a href="#Chatroom.fetch_chatter" class="hidden" class="h4" id="Chatroom.fetch_chatter">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_chatter
</a>

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
<span style="margin-left: 30px">    The chatter</span><br>


<a href="#Chatroom.fetch_bans" class="hidden" class="h4" id="Chatroom.fetch_bans">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_bans
</a>

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
<span style="margin-left: 30px">    Yields all of the ban entries</span><br>


<a href="#Chatroom.fetch_banned_words" class="hidden" class="h4" id="Chatroom.fetch_banned_words">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_banned_words
</a>

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
<span style="margin-left: 30px">    A list of the banned words</span><br>


<a href="#Chatroom.fetch_rules" class="hidden" class="h4" id="Chatroom.fetch_rules">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_rules
</a>

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
<span style="margin-left: 30px">    The rules</span><br>


<a href="#Chatroom.fetch_poll" class="hidden" class="h4" id="Chatroom.fetch_poll">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_poll
</a>

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
<span style="margin-left: 30px">    The poll</span><br>


<a href="#Chatroom.fetch_emotes" class="hidden" class="h4" id="Chatroom.fetch_emotes">
    <span class="async">
        async def 
    </span>
    Chatroom.fetch_emotes
</a>

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
<span style="margin-left: 30px">    Yields each emote. Starting with from the chatroom, then global</span><br>

# BanEntry


<a href="#BanEntry" class="hidden" class="h4" id="BanEntry">
    <span class="class">
        class 
    </span>
    BanEntry
</a>

<br>
A dataclass which represents a ban entry on kick.<br>
This includes timeouts.<br>
<br>
<span class="h4">Attributes</span><br>
reason: str<br>
<span style="margin-left: 30px">    The reason for the ban/timeout</span><br>
is_permanent: bool<br>
<span style="margin-left: 30px">    wether the ban is permanent. True == ban, false == timeout</span><br>
user: <a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden">`PartialUser`</a></a></a></a><br>
<span style="margin-left: 30px">    The user the action was towards</span><br>
banned_by: <a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden">`PartialUser`</a></a></a></a><br>
<span style="margin-left: 30px">    The responsible mod</span><br>
expires_at: datetime.datetime | None<br>
<span style="margin-left: 30px">    when the timeout expires at. None for a ban</span><br>
banned_at: datetime.datetime<br>
<span style="margin-left: 30px">    When the action happened</span><br>
chatroom: Chatroom<br>
<span style="margin-left: 30px">    The chatroom the action happened in</span><br>

## Methods


<a href="#BanEntry.unban" class="hidden" class="h4" id="BanEntry.unban">
    <span class="async">
        async def 
    </span>
    BanEntry.unban
</a>

<br>
Unbans the chatter from the chatroom.<br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    Streamer or chatter not found</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Unbanning the chatter failed</span><br>
Forbidden<br>
<span style="margin-left: 30px">    You are unauthorized from unbanning the chatter</span><br>

# Users


<a href="#User" class="hidden" class="h4" id="User">
    <span class="class">
        class 
    </span>
    User
</a>

<br>
A dataclass which represents a User on kick<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    The user's id</span><br>
username: str<br>
<span style="margin-left: 30px">    The user's name</span><br>
state: str<br>
<span style="margin-left: 30px">    The state the user has said they live in</span><br>
socials: <a href="#Socials" class="hidden">`Socials`</a><br>
<span style="margin-left: 30px">    The socials the user has said they have</span><br>
country: str<br>
<span style="margin-left: 30px">    The country the user has said they live in</span><br>
playback_url: str<br>
<span style="margin-left: 30px">    The user's playback url</span><br>
slug: str<br>
<span style="margin-left: 30px">    The user's slug</span><br>
vod_enabled: bool<br>
<span style="margin-left: 30px">    If the user has vods enabled</span><br>
is_banned: bool<br>
<span style="margin-left: 30px">    If the user is banned</span><br>
subscription_enabled: bool<br>
<span style="margin-left: 30px">    If the user has subscriptions enabled</span><br>
follower_count: int<br>
<span style="margin-left: 30px">    The amount of followers the user has</span><br>
subscriber_badges: list[<a href="#SubscriberBadge" class="hidden">`SubscriberBadge`</a>]<br>
<span style="margin-left: 30px">    A list of subscriber badges the user has</span><br>
online_banner: <a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden">`Asset`</a></a></a></a></a></a></a></a></a> | None<br>
<span style="margin-left: 30px">    the banner that gets displayed when the user is live</span><br>
offline_banner: <a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden">`Asset`</a></a></a></a></a></a></a></a></a> | None<br>
<span style="margin-left: 30px">    the banner that gets displayed when the user is offline</span><br>
is_muted: bool<br>
<span style="margin-left: 30px">    If the user is muted</span><br>
is_verified: bool<br>
<span style="margin-left: 30px">    If the user is verified</span><br>
avatar: <a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden">`Asset`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    The user's avatar</span><br>
can_host: bool<br>
<span style="margin-left: 30px">    If the user can host</span><br>
bio: str<br>
<span style="margin-left: 30px">    The user's bio</span><br>
agreed_to_terms: bool<br>
<span style="margin-left: 30px">    if the user has agreed to kick's TOS</span><br>
email_verified_at: datetime.datetime<br>
<span style="margin-left: 30px">    When the user verified their user</span><br>
livestream: <a href="#Livestream" class="hidden">`Livestream`</a> | None<br>
<span style="margin-left: 30px">    The user's livestream</span><br>
chatroom: <a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden">`Chatroom`</a></a></a></a><br>
<span style="margin-left: 30px">    The user's chatroom</span><br>
recent_categories: list[<a href="#Category" class="hidden"><a href="#Category" class="hidden"><a href="#Category" class="hidden">`Category`</a></a></a>]<br>
<span style="margin-left: 30px">    The categories the user has recently gone live in</span><br>

## Methods

{{User.fetch_videos}}
[[User.fetch_videos]]

{{User.fetch_gift_leaderboard}}
[[User.fetch_gift_leaderboard]]

<hr>


<a href="#PartialUser" class="hidden" class="h4" id="PartialUser">
    <span class="class">
        class 
    </span>
    PartialUser
</a>

<br>
This dataclass represents a partial user on kick<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    The user's id</span><br>
username: str<br>
<span style="margin-left: 30px">    The user's name</span><br>

<hr>


<a href="#ClientUser" class="hidden" class="h4" id="ClientUser">
    <span class="class">
        class 
    </span>
    ClientUser
</a>



## Methods


<a href="#ClientUser.fetch_videos" class="hidden" class="h4" id="ClientUser.fetch_videos">
    <span class="def">
        def 
    </span>
    ClientUser.fetch_videos
</a>



<hr>


<a href="#Chatter" class="hidden" class="h4" id="Chatter">
    <span class="class">
        class 
    </span>
    Chatter
</a>

<br>
A dataclass which respresents a chatter on kick<br>
<br>
<span class="h4">Attributes</span><br>
chatroom: Chatroom<br>
<span style="margin-left: 30px">    The chatroom the chatter is in</span><br>
id: int<br>
<span style="margin-left: 30px">    The chatter's id</span><br>
username: str<br>
<span style="margin-left: 30px">    The chatter's username</span><br>
slug: str<br>
<span style="margin-left: 30px">    The chatter' slug</span><br>
avatar: <a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden">`Asset`</a></a></a></a></a></a></a></a></a> | None<br>
<span style="margin-left: 30px">    The chatter's avatar, if any</span><br>
is_staff: bool<br>
<span style="margin-left: 30px">    If the chatter is a staff member in the chatroom</span><br>
is_owner: bool<br>
<span style="margin-left: 30px">    If the chatter is the chatroom owner</span><br>
is_mod: bool<br>
<span style="margin-left: 30px">    If the chatter is a mod in the chatroom</span><br>
badges: list[<a href="#ChatBadge" class="hidden">`ChatBadge`</a>]<br>
<span style="margin-left: 30px">    The chat badges the chatter has</span><br>
following_since: datetime.datetime | None<br>
<span style="margin-left: 30px">    when the chatter started following the streamer</span><br>

## Methods


<a href="#Chatter.ban" class="hidden" class="h4" id="Chatter.ban">
    <span class="async">
        async def 
    </span>
    Chatter.ban
</a>

<br>
Permanently bans a user from a chatroom.<br>
<br>
<span class="h4">Parameters</span><br>
reason: str<br>
<span style="margin-left: 30px">    The reason for the ban</span><br>
<br>
<span class="h4">Raises</span><br>
<a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden">`HTTPException`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Banning the user failed</span><br>
<a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden">`Forbidden`</a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    You are unauthorized from banning the user</span><br>
<a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden">`NotFound`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Streamer or user not found</span><br>


<a href="#Chatter.unban" class="hidden" class="h4" id="Chatter.unban">
    <span class="async">
        async def 
    </span>
    Chatter.unban
</a>

<br>
Unbans the chatter from the chatroom<br>
<br>
<span class="h4">Raises</span><br>
<a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden">`HTTPException`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Unbanning the user failed</span><br>
<a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden">`Forbidden`</a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    You are unauthorized from unbanning the user</span><br>
<a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden">`NotFound`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Streamer or user not found</span><br>


<a href="#Chatter.timeout" class="hidden" class="h4" id="Chatter.timeout">
    <span class="async">
        async def 
    </span>
    Chatter.timeout
</a>

<br>
Times out a user for a given amount of time.<br>
<br>
<span class="h4">Parameters</span><br>
duration: int<br>
<span style="margin-left: 30px">    The amount of seconds for the timeout to be</span><br>
reason: str<br>
<span style="margin-left: 30px">    The reason for the timeout</span><br>
<br>
<span class="h4">Raises</span><br>
<a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden">`HTTPException`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    timing out the user failed</span><br>
<a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden">`Forbidden`</a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    You are unauthorized from timing out the user</span><br>
<a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden">`NotFound`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Streamer or user not found</span><br>


<a href="#Chatter.untimeout" class="hidden" class="h4" id="Chatter.untimeout">
    <span class="async">
        async def 
    </span>
    Chatter.untimeout
</a>

<br>
untimeout's the chatter<br>
<br>
<span class="h4">Raises</span><br>
<a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden">`HTTPException`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    untimeouting the user failed</span><br>
<a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden">`Forbidden`</a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    You are unauthorized from untimeouting the user</span><br>
<a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden">`NotFound`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Streamer or user not found</span><br>

<hr>


<a href="#PartialChatter" class="hidden" class="h4" id="PartialChatter">
    <span class="class">
        class 
    </span>
    PartialChatter
</a>

<br>
This represents a partial user.<br>
<br>
<span class="h4">Attributes</span><br>
streamer_name: str<br>
<span style="margin-left: 30px">    The streamer's name</span><br>
username: str<br>
<span style="margin-left: 30px">    The chatter's username</span><br>

## Methods


<a href="#PartialChatter.to_user" class="hidden" class="h4" id="PartialChatter.to_user">
    <span class="async">
        async def 
    </span>
    PartialChatter.to_user
</a>

<br>
Fetches a user object for the chatter<br>
<br>
<span class="h4">Raises</span><br>
<a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden">`HTTPException`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Fetching the user failed</span><br>
<a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden">`NotFound`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    User not found</span><br>
<br>
<span class="h4">Returns</span><br>
<a href="#User" class="hidden"><a href="#User" class="hidden"><a href="#User" class="hidden">`User`</a></a></a><br>
<span style="margin-left: 30px">    The user</span><br>


<a href="#PartialChatter.ban" class="hidden" class="h4" id="PartialChatter.ban">
    <span class="async">
        async def 
    </span>
    PartialChatter.ban
</a>

<br>
Permanently bans a user from a chatroom.<br>
<br>
<span class="h4">Parameters</span><br>
reason: str<br>
<span style="margin-left: 30px">    The reason for the ban</span><br>
<br>
<span class="h4">Raises</span><br>
<a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden">`HTTPException`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Banning the user failed</span><br>
<a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden">`Forbidden`</a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    You are unauthorized from banning the user</span><br>
<a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden">`NotFound`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Streamer or user not found</span><br>


<a href="#PartialChatter.unban" class="hidden" class="h4" id="PartialChatter.unban">
    <span class="async">
        async def 
    </span>
    PartialChatter.unban
</a>

<br>
Unbans the chatter from the chatroom<br>
<br>
<span class="h4">Raises</span><br>
<a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden">`HTTPException`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Unbanning the user failed</span><br>
<a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden">`Forbidden`</a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    You are unauthorized from unbanning the user</span><br>
<a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden">`NotFound`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Streamer or user not found</span><br>


<a href="#PartialChatter.timeout" class="hidden" class="h4" id="PartialChatter.timeout">
    <span class="async">
        async def 
    </span>
    PartialChatter.timeout
</a>

<br>
Times out a user for a given amount of time.<br>
<br>
<span class="h4">Parameters</span><br>
duration: int<br>
<span style="margin-left: 30px">    The amount of seconds for the timeout to be</span><br>
reason: str<br>
<span style="margin-left: 30px">    The reason for the timeout</span><br>
<br>
<span class="h4">Raises</span><br>
<a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden">`HTTPException`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    timing out the user failed</span><br>
<a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden">`Forbidden`</a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    You are unauthorized from timing out the user</span><br>
<a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden">`NotFound`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Streamer or user not found</span><br>


<a href="#PartialChatter.untimeout" class="hidden" class="h4" id="PartialChatter.untimeout">
    <span class="async">
        async def 
    </span>
    PartialChatter.untimeout
</a>

<br>
untimeout's the chatter<br>
<br>
<span class="h4">Raises</span><br>
<a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden"><a href="#HTTPException" class="hidden">`HTTPException`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    untimeouting the user failed</span><br>
<a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden"><a href="#Forbidden" class="hidden">`Forbidden`</a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    You are unauthorized from untimeouting the user</span><br>
<a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden"><a href="#NotFound" class="hidden">`NotFound`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    Streamer or user not found</span><br>

<hr>


<a href="#Author" class="hidden" class="h4" id="Author">
    <span class="class">
        class 
    </span>
    Author
</a>

<br>
Represents the author of a message on kick<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    The author's id</span><br>
slug: str<br>
<span style="margin-left: 30px">    The author's slug</span><br>
color: str<br>
<span style="margin-left: 30px">    The authors... color?</span><br>
badges: list<br>
<span style="margin-left: 30px">    Unknown</span><br>

# Messages


<a href="#Message" class="hidden" class="h4" id="Message">
    <span class="class">
        class 
    </span>
    Message
</a>

<br>
Represents a message sent on kick<br>
<br>
<span class="h4">Attributes</span><br>
id: str<br>
<span style="margin-left: 30px">    the message's id</span><br>
is_reply: bool<br>
<span style="margin-left: 30px">    If the message is replying to any message</span><br>
references: <a href="#PartialMessage" class="hidden"><a href="#PartialMessage" class="hidden">`PartialMessage`</a></a> | None<br>
<span style="margin-left: 30px">    If the message is replying to a message, a <a href="#PartialMessage" class="hidden"><a href="#PartialMessage" class="hidden">`PartialMessage`</a></a> object is returned. Otherwise None</span><br>
chatroom_id: int<br>
<span style="margin-left: 30px">    The id of the chatroom the message was sent in</span><br>
chatroom: <a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden">`Chatroom`</a></a></a></a> | None<br>
<span style="margin-left: 30px">    The chatroom the message was sent in.</span><br>
content: str<br>
<span style="margin-left: 30px">    The message's content</span><br>
created_at: datetime.datetime<br>
<span style="margin-left: 30px">    When the message was sent</span><br>
author: <a href="#Author" class="hidden">`Author`</a><br>
<span style="margin-left: 30px">    The message's author</span><br>

<hr>


<a href="#PartialMessage" class="hidden" class="h4" id="PartialMessage">
    <span class="class">
        class 
    </span>
    PartialMessage
</a>

<br>
This represents a partial message. Mainly used as the message someone is replying too.<br>
<br>
<span class="h4">Attributes</span><br>
id: str<br>
<span style="margin-left: 30px">    The message's id</span><br>
content: str<br>
<span style="margin-left: 30px">    The message's content</span><br>
author: <a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden"><a href="#PartialUser" class="hidden">`PartialUser`</a></a></a></a><br>
<span style="margin-left: 30px">    The message's author</span><br>

# Emote


<a href="#Emote" class="hidden" class="h4" id="Emote">
    <span class="class">
        class 
    </span>
    Emote
</a>

<br>
A dataclass which represents an emote on kick.<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    The emote's id</span><br>
is_global: bool<br>
<span style="margin-left: 30px">    If the emote is a global emote, or from a channel</span><br>
channel_id: int | None<br>
<span style="margin-left: 30px">    returns the channel_id the emote is from, or None if global</span><br>
name: str<br>
<span style="margin-left: 30px">    The emote's name</span><br>
subscribers_only: bool<br>
<span style="margin-left: 30px">    If you have to be a subscriber of the channel to use it. False for global emotes</span><br>
source: <a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden">`Asset`</a></a></a></a></a></a></a></a></a><br>
<span style="margin-left: 30px">    An asset which contains the emote's source.</span><br>

# Enums


<a href="#ChatroomChatMode" class="hidden" class="h4" id="ChatroomChatMode">
    <span class="class">
        class 
    </span>
    ChatroomChatMode
</a>

<br>
An enum containing possble chatroom chat mode values.<br>
<br>
<span class="h4">Attributes</span><br>
public: <a href="#ChatroomChatMode" class="hidden"><a href="#ChatroomChatMode" class="hidden">`ChatroomChatMode`</a></a><br>
<span style="margin-left: 30px">    The public value</span><br>
privet: <a href="#ChatroomChatMode" class="hidden"><a href="#ChatroomChatMode" class="hidden">`ChatroomChatMode`</a></a><br>
<span style="margin-left: 30px">    The privet value</span><br>

# Leaderboard


<a href="#GiftLeaderboardEntry" class="hidden" class="h4" id="GiftLeaderboardEntry">
    <span class="class">
        class 
    </span>
    GiftLeaderboardEntry
</a>

<br>
This dataclass represents a gift leaderboard entry.<br>
<br>
<span class="h4">Attributes</span><br>
user_id: int<br>
<span style="margin-left: 30px">    The id of the user with this entry</span><br>
quantity: int<br>
<span style="margin-left: 30px">    The amount of subs this person has gifted</span><br>
username: str<br>
<span style="margin-left: 30px">    The user's username</span><br>

<hr>


<a href="#GiftLeaderboard" class="hidden" class="h4" id="GiftLeaderboard">
    <span class="class">
        class 
    </span>
    GiftLeaderboard
</a>

<br>
This is a dataclass which reprsents the gift leaderboard for a kick streamer.<br>
<br>
<span class="h4">Attributes</span><br>
streamer: <a href="#User" class="hidden"><a href="#User" class="hidden"><a href="#User" class="hidden">`User`</a></a></a><br>
<span style="margin-left: 30px">    The streamer that the leaderboard is for</span><br>
this_week: list[<a href="#GiftLeaderboardEntry" class="hidden"><a href="#GiftLeaderboardEntry" class="hidden"><a href="#GiftLeaderboardEntry" class="hidden">`GiftLeaderboardEntry`</a></a></a>]<br>
<span style="margin-left: 30px">    The gift leaderboard for the current week</span><br>
this_month: list[<a href="#GiftLeaderboardEntry" class="hidden"><a href="#GiftLeaderboardEntry" class="hidden"><a href="#GiftLeaderboardEntry" class="hidden">`GiftLeaderboardEntry`</a></a></a>]<br>
<span style="margin-left: 30px">    The gift leaderboard for the current month</span><br>
all_time: list[<a href="#GiftLeaderboardEntry" class="hidden"><a href="#GiftLeaderboardEntry" class="hidden"><a href="#GiftLeaderboardEntry" class="hidden">`GiftLeaderboardEntry`</a></a></a>]<br>
<span style="margin-left: 30px">    The gift leaderboard for all time</span><br>

# Livestream


<a href="#Livestream" class="hidden" class="h4" id="Livestream">
    <span class="class">
        class 
    </span>
    Livestream
</a>

<br>
A dataclass which represents a livestream on kick.<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    probably the livestream's id</span><br>
slug: str<br>
<span style="margin-left: 30px">    The streamer's slug</span><br>
channel_id: int<br>
<span style="margin-left: 30px">    probably the streamer's id or the chatroom id</span><br>
created_at: datetime.datetime<br>
<span style="margin-left: 30px">    When the livestream started</span><br>
title: str<br>
<span style="margin-left: 30px">    The livestream's title</span><br>
is_live: bool<br>
<span style="margin-left: 30px">    If the livestream is currently live</span><br>
thumbnail: <a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden">`Asset`</a></a></a></a></a></a></a></a></a> | None<br>
<span style="margin-left: 30px">    Returns the livestream's thumbnail if it has one</span><br>
duration: int<br>
<span style="margin-left: 30px">    Probably how long the livestream is/was in seconds</span><br>
language: str<br>
<span style="margin-left: 30px">    The language the livestream is in</span><br>
is_mature: bool<br>
<span style="margin-left: 30px">    If the livestream is marked as 18+</span><br>
viewer_count: int<br>
<span style="margin-left: 30px">    The amount of people currently watching</span><br>
tags: list[str]<br>
<span style="margin-left: 30px">    Tags applied to the livestream</span><br>
url: str<br>
<span style="margin-left: 30px">    The livestream's url</span><br>
embed_url: str<br>
<span style="margin-left: 30px">    The livestream's player/embed url</span><br>
categories: list[<a href="#Category" class="hidden"><a href="#Category" class="hidden"><a href="#Category" class="hidden">`Category`</a></a></a>]<br>
<span style="margin-left: 30px">    The categories the livestream is in</span><br>

# Polls


<a href="#PollOption" class="hidden" class="h4" id="PollOption">
    <span class="class">
        class 
    </span>
    PollOption
</a>

<br>
This dataclass represents a chatroom <a href="#Poll" class="hidden">`Poll`</a>'s option on kick.<br>
<br>
<span class="h4">Attributes</span><br>
chatroom: <a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden">`Chatroom`</a></a></a></a><br>
<span style="margin-left: 30px">    The chatroom the poll is in</span><br>
id: int<br>
<span style="margin-left: 30px">    The option's id</span><br>
label: str<br>
<span style="margin-left: 30px">    The option's label</span><br>
votes: int<br>
<span style="margin-left: 30px">    The amount of votes the option has</span><br>

## Methods


<a href="#PollOption.vote" class="hidden" class="h4" id="PollOption.vote">
    <span class="async">
        async def 
    </span>
    PollOption.vote
</a>

<br>
Votes for this option in the poll<br>
<br>
<span class="h4">Raises</span><br>
NotFound<br>
<span style="margin-left: 30px">    There is no poll in the current chatroom</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Deleting the poll failed</span><br>

<hr>


<a href="#Poll" class="hidden" class="h4" id="Poll">
    <span class="class">
        class 
    </span>
    Poll
</a>

<br>
This dataclass represents a poll in a chatroom on kick.<br>
<br>
<span class="h4">Attributes</span><br>
chatroom: <a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden"><a href="#Chatroom" class="hidden">`Chatroom`</a></a></a></a><br>
<span style="margin-left: 30px">    The chatroom the poll is in</span><br>
title: str<br>
<span style="margin-left: 30px">    The poll's title</span><br>
options: list[<a href="#PollOption" class="hidden">`PollOption`</a>]<br>
<span style="margin-left: 30px">    The poll's options</span><br>
duration: int<br>
<span style="margin-left: 30px">    How long the poll will last in seconds</span><br>
result_display_duration: int<br>
<span style="margin-left: 30px">    How long the poll will display the results in seconds</span><br>
has_voted: bool<br>
<span style="margin-left: 30px">    if you've voted yet</span><br>
ends_at: datetime.datetime<br>
<span style="margin-left: 30px">    When the poll ends at</span><br>

## Methods


<a href="#Poll.delete" class="hidden" class="h4" id="Poll.delete">
    <span class="async">
        async def 
    </span>
    Poll.delete
</a>

<br>
Deletes the current poll from the chatroom<br>
<br>
<span class="h4">Raises</span><br>
Forbidden<br>
<span style="margin-left: 30px">    You are unauthorized to delete the poll</span><br>
NotFound<br>
<span style="margin-left: 30px">    There is no poll in the current chatroom</span><br>
HTTPException<br>
<span style="margin-left: 30px">    Deleting the poll failed</span><br>

# Videos


<a href="#Video" class="hidden" class="h4" id="Video">
    <span class="class">
        class 
    </span>
    Video
</a>

<br>
This dataclass represents a video on kick<br>
<br>
<span class="h4">Attributes</span><br>
id: int<br>
<span style="margin-left: 30px">    The video's id</span><br>
slug: str<br>
<span style="margin-left: 30px">    the video's slug</span><br>
channel_id: int<br>
<span style="margin-left: 30px">    Probably the id of the channel the video is from</span><br>
created_at: datetime.datetime<br>
<span style="margin-left: 30px">    When the video was created</span><br>
updated_at: datetime.datetime<br>
<span style="margin-left: 30px">    When the video was last updated</span><br>
title: str<br>
<span style="margin-left: 30px">    The video's title</span><br>
live_stream_id: int<br>
<span style="margin-left: 30px">    The id of the live stream the video is from</span><br>
thumbnail: <a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden"><a href="#Asset" class="hidden">`Asset`</a></a></a></a></a></a></a></a></a> | None<br>
<span style="margin-left: 30px">    The video's thumbnail</span><br>
duration: int<br>
<span style="margin-left: 30px">    How long the video is in seconds</span><br>
language: str<br>
<span style="margin-left: 30px">    The language the video is in</span><br>
is_mature: bool<br>
<span style="margin-left: 30px">    If the video is marked as 18+</span><br>
viewer_count: int<br>
<span style="margin-left: 30px">    How many people have seen the video</span><br>
categories: list[<a href="#Category" class="hidden"><a href="#Category" class="hidden"><a href="#Category" class="hidden">`Category`</a></a></a>]<br>
<span style="margin-left: 30px">    The categories the video is in</span><br>

# Other


<a href="#Socials" class="hidden" class="h4" id="Socials">
    <span class="class">
        class 
    </span>
    Socials
</a>

<br>
The socials a user on kick has added to their profile<br>
<br>
<span class="h4">Attributes</span><br>
instagram: str<br>
<span style="margin-left: 30px">    Their instagram</span><br>
youtube: str<br>
<span style="margin-left: 30px">    Their youtube</span><br>
twitter: str<br>
<span style="margin-left: 30px">    Their twitter</span><br>
discord: str<br>
<span style="margin-left: 30px">    Their discord</span><br>
tiktok: str<br>
<span style="margin-left: 30px">    Their tiktok</span><br>
facebook: str<br>
<span style="margin-left: 30px">    Their facebook</span><br>

# Errors


<a href="#CloudflareBypassException" class="hidden" class="h4" id="CloudflareBypassException">
    <span class="class">
        class 
    </span>
    CloudflareBypassException
</a>

<br>
This error is used when there is an error with the bypass script.<br>

<hr>


<a href="#KickException" class="hidden" class="h4" id="KickException">
    <span class="class">
        class 
    </span>
    KickException
</a>

<br>
This error is used when there is an error with kick.<br>

<hr>


<a href="#LoginFailure" class="hidden" class="h4" id="LoginFailure">
    <span class="class">
        class 
    </span>
    LoginFailure
</a>

<br>
This error is used when there is an error with logging in.<br>

<hr>


<a href="#HTTPException" class="hidden" class="h4" id="HTTPException">
    <span class="class">
        class 
    </span>
    HTTPException
</a>

<br>
This error is used when an error is ran into when making a request to kick.<br>
<br>
<span class="h4">Attributes</span><br>
status_code: int<br>
<span style="margin-left: 30px">    The HTTP code</span><br>

<hr>


<a href="#Forbidden" class="hidden" class="h4" id="Forbidden">
    <span class="class">
        class 
    </span>
    Forbidden
</a>

<br>
This error is used when kick returns a 403 status code.<br>
<br>
<span class="h4">Attributes</span><br>
status_code: int = 403<br>
<span style="margin-left: 30px">    The HTTP code</span><br>

<hr>


<a href="#NotFound" class="hidden" class="h4" id="NotFound">
    <span class="class">
        class 
    </span>
    NotFound
</a>

<br>
This error is used when kick returns a 404 status code.<br>
<br>
<span class="h4">Attributes</span><br>
status_code: int = 404<br>
<span style="margin-left: 30px">    The HTTP code</span><br>

<hr>


<a href="#InternalKickException" class="hidden" class="h4" id="InternalKickException">
    <span class="class">
        class 
    </span>
    InternalKickException
</a>

<br>
This error is used when kick returns a a 500 status code, or doesn't connect.<br>
<br>
<span class="h4">Attributes</span><br>
status_code: int = 500<br>
<span style="margin-left: 30px">    The HTTP code</span><br>
