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

    # Fetching the chatroom's poll
    poll = await chatroom.fetch_poll()

    # Getting the first option
    option = poll.options[0]

    # Voting for the first option
    await option.vote()

    # Refetching the poll to get an updated votes count
    new_poll = await chatroom.fetch_poll()

    # Getting the new first option
    new_option = new_poll.options[0]

    # Printing the updated vote count
    print(f"The first option now has {new_option.votes} votes.")


# You can also pass the `credentials` arg to authenticate yourself
# Authentication is not required for listening to messages
client.run()
