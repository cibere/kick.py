import asyncio
from kick import Client
from kick import Credentials

async def login():
    creds = Credentials(username="testingkicker",  password="TestingKicker123.")
    client = Client()
    await client.login(creds)
    print(client.user)
    res = await client.search_categories("Ageof")
    print(res.hits[0])
    print(int(res.hits[0].document.category_id))
    setRes = await client.set_stream_info("flerking", "English", res.hits[0].document.name, int(res.hits[0].document.id), False)
    print(setRes.title)
    await client.close()

async def main():
    await login()

if __name__ == "__main__":
    asyncio.run(main())
