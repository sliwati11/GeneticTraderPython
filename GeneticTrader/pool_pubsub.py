import asyncio
import aioredis


STOPWORD = 'STOP'


async def pubsub():
    pool = await aioredis.create_pool('redis://localhost', minsize=5, maxsize=10)

    async def reader(channel):
        while await channel.wait_message():
            msg = await channel.get(encoding='utf-8')
            # ... process message ...
            print("message salwa in {}: {}".format(channel.name, msg))

            if msg == STOPWORD:
                return

    '''with await pool as conn:
        await conn.execute_pubsub('subscribe', 'TraderReady')
        channel = conn.pubsub_channels['TraderReady']
        await reader(channel)  # wait for reader to complete
       # await conn.execute_pubsub('unsubscribe', 'TraderReady:1')
'''
    # Explicit connection usage
    conn = await pool.acquire()
    try:
        await conn.execute_pubsub('subscribe', 'TraderReady:')
        await conn.execute_pubsub('subscribe', 'TraderReady')
        channel1 = conn.pubsub_channels['TraderReady:']
        channel2 = conn.pubsub_channels['TraderReady']
        await reader(channel1)  # wait for reader to complete
        await reader(channel2)  # wait for reader to complete
        #await conn.execute_pubsub('unsubscribe', 'TraderReady:1')
    finally:
        pool.release(conn)

    pool.close()
    await pool.wait_closed()    # closing all open connections


def main():
    loop = asyncio.get_event_loop()
    tsk = asyncio.ensure_future(pubsub(), loop=loop)

    async def publish():
        pub = await aioredis.create_redis(
            'redis://localhost')
        while not tsk.done():
            # wait for clients to subscribe
            while True:
                subs = await pub.pubsub_numsub('TraderReady:')
                if subs[b'TraderReady:'] == 1:
                    break
                await asyncio.sleep(0, loop=loop)
            # publish some messages
            for msg in ['one', 'two', 'three']:
                await pub.publish('TraderReady:', msg)
            # send stop word
            await pub.publish('TraderReady:', STOPWORD)
        pub.close()
        await pub.wait_closed()

    loop.run_until_complete(asyncio.gather(publish(), tsk, loop=loop))


if __name__ == '__main__':
    import os
    if 'redis_version:2.6' not in os.environ.get('REDIS_VERSION', ''):
        main()