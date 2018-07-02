import asyncio
import aioredis

class RedisSubscriber:


    #@asyncio.coroutine
    async def connect(self):
        self._connection = await aioredis.create_redis(('localhost', 6379))


    #@asyncio.coroutine
    async def subscribe(self, channel):
        await self._connection.subscribe(channel)

    #@asyncio.coroutine
    async def get(self):
        channel, reply = await self._connection.listen()  # this is made up
        return channel, reply