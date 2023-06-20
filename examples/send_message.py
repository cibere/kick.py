from kick import Client

client = Client()


@client.event
async def on_ready():
    print("I have successfully logged in")

    username = (
        "xqc"  # The username/slug of the user's chat you want to send the message in
    )
    user = await client.fetch_user(username)
    chatroom = user.chatroom

    await chatroom.send("Hello!")


# You can also pass the `credentials` arg to authenticate yourself
# Authentication is not required for listening to messages
client.run()
