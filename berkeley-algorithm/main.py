import asyncio
from client import Client
from master import Master 


async def main():
    master = Master()
    asyncio.create_task(master.start())

    await asyncio.sleep(1)

    client1 = Client(1)
    client2 = Client(2)
    client3 = Client(3)
    client4 = Client(4)
    client5 = Client(5)
    client6 = Client(6)
    client7 = Client(7)
    client8 = Client(8)
    client9 = Client(9)
    client10 = Client(10)
    client11 = Client(11)
    client12 = Client(12)
    client13 = Client(13)
    client14 = Client(14)
    client15 = Client(15)
    client16 = Client(16)

    await asyncio.gather(
        asyncio.create_task(client1.connect()),
        asyncio.create_task(client2.connect()),
        asyncio.create_task(client3.connect()),
        asyncio.create_task(client4.connect()),
        asyncio.create_task(client5.connect()),
        asyncio.create_task(client6.connect()),
        asyncio.create_task(client7.connect()),
        asyncio.create_task(client8.connect()),
        asyncio.create_task(client9.connect()),
        asyncio.create_task(client10.connect()),
        asyncio.create_task(client11.connect()),
        asyncio.create_task(client12.connect()),
        asyncio.create_task(client13.connect()),
        asyncio.create_task(client14.connect()),
        asyncio.create_task(client15.connect()),
        asyncio.create_task(client16.connect()),
    )


if __name__ == "__main__":
    asyncio.run(main())

