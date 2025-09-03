import asyncio
from typing import List
from clock import Clock
import websockets


class Slave:
    def __init__(self, websocket):
        self.websocket = websocket

    def set_time(self, time):
        self.time = float(time)

    def set_offset(self, offset):
        self.offset = offset


class Master:
    def __init__(self):
        self.clock = Clock()
        self.slaves: List[Slave] = []
        self.current_time = self.clock.randomize_clock()

    async def start(self):
        print(f"[M] - Master time: {self.clock.seconds_to_hours(self.current_time)}")

        async with websockets.serve(self.handler, "localhost", 8000):
            await asyncio.Future()

    async def handler(self, websocket):
        slave = Slave(websocket)
        self.slaves.append(slave)

        try:
            await websocket.send(str(self.current_time))

            response = await websocket.recv()
            slave.set_time(self.current_time + float(response))
            slave.set_offset(float(response))

            await self.berkeley_algorithm()

            await websocket.recv()
        except Exception as e:
            print(f"[M] - Master error: {e}")
        finally:
            self.slaves.remove(slave)

    async def berkeley_algorithm(self):
        if all(hasattr(s, "time") for s in self.slaves):
            total_time = sum(s.offset for s in self.slaves)
            self.current_time += total_time / (len(self.slaves) + 1)

            for slave in self.slaves:
                await slave.websocket.send(str(self.calculate_time_difference(slave)))

            print(f"[M] - New master time: {self.clock.seconds_to_hours(self.current_time)}")

    def calculate_time_difference(self, slave: Slave):
        return self.current_time - slave.time
