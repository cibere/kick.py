from kick import Client, Credentials, user

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


# You have to authenticate yourself in order to send mesages
credentials = Credentials(
    username="...",  # you can also use the email kwarg, but not both
    password="...",
)
client.run(credentials)
