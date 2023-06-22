from kick import Client, Message

client = Client()


@client.event
async def on_message(msg: Message):
    print(f"Received message by {msg.author.slug} saying {msg.content}")


@client.event
async def on_ready():
    print("I have successfully logged in")

    username = "xqc"  # The username/slug of the user's chat you want to listen to
    user = await client.fetch_user(username)
    await user.chatroom.connect()


# You can also pass the `credentials` arg to authenticate yourself
# Authentication is not required for listening to messages
client.run()
