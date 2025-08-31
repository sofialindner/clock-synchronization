import asyncio
from client import Client
from server import Server

async def main():
    server = Server()
    asyncio.create_task(server.start())

    client1 = Client()
    client2 = Client()

    await asyncio.gather(
        asyncio.create_task(client1.connect()),
        asyncio.create_task(client2.connect()),
    )

if __name__ == "__main__":
    asyncio.run(main())