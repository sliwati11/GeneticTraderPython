import json
import aioredis
import asyncio

class RedisManager:

    def __init__(self, pool=None):
        #self. pool = None #
        self.pool = pool #asyncio.async(self.createPool())
        self.publisher = None
        self.inputData = None

    async def createPool(self):
        if self.pool is None:

            self.pool = await aioredis.create_pool('redis://localhost', minsize=5, maxsize=10)

        return self.pool

    async def reader(self, channel):
        '''conn = await self.pool.acquire()
            print('conn'+ str(conn))
            try:
            channel = conn.pubsub_channels['TraderReady:1']'''

        while await channel.wait_message():
            msg = await channel.get(encoding='utf-8')
            # print('inputData initRedis', self.inputData)

            if channel.name == b'TraderReady':
                self.inputData = json.loads(msg)
                print('Channel: TraderReady')

            return json.loads(msg)


    async def async_get(self, key):
        async with self.pool.get() as conn:
            value = await conn.execute('get', key)
            print(str(key)+' : ' + str(value))
        return value

    async def async_set(self, key, value):
        async with self.pool.get() as conn:
            value = await conn.execute('set', key, value)
            print('SET: '+str(key) + ' : ' + str(value))


    async def subscribe(self, channel):
        print('self.pool:'+str(self.pool))
        conn = await self.pool.acquire()
        try:
            await conn.execute_pubsub('subscribe', channel) #str(channel)
            chanel = conn.pubsub_channels[channel]
            print('chanel: ' + channel)

            ''' wait for reader to complete '''
            await self.reader(chanel)
            print('inputData subscribe'+ str(self.inputData))
            await conn.execute_pubsub('unsubscribe', 'TraderReady')

        finally:
            'returns used connection back into pool.'
            self.pool.release(conn)

    async def publish(self, channel, msg):
        self.publisher = await aioredis.create_redis('redis://localhost')
        await self.publisher.publish(channel, msg)
        self.publisher.close()