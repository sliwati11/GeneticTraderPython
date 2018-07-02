import asyncio
import aioredis
from aioredis.pubsub import Receiver
#import RedisSubscriber

mpsc = Receiver()
loop = asyncio.get_event_loop()
async def single_reader():
    while await mpsc.wait_message():
        sender, message = await mpsc.get()
        print("Got message {!r} from {!r}", message, sender.name)

async def reader(ch):
    while await ch.wait_message():
        msg = await ch.get_json()
        print("Got Message:", msg)


async def main():
    pub = await aioredis.create_redis(
        'redis://localhost')
    sub = await aioredis.create_redis(
        'redis://localhost')
    #res = await sub.subscribe('TraderReady:')
    #ch1 = res[0]

    #tsk = asyncio.ensure_future(reader(ch1))

    # run reader
    asyncio.ensure_future(single_reader())
    # use mpsc to add channles
    await sub.subscribe(
        mpsc.channel('TraderReady:'),
        mpsc.channel('InRedis:')
    )

    res = await pub.publish_json('TraderReady', ["Hello", "world"])
    assert res == 1
    print('res: ', res)
    await sub.psubscribe(mpsc.pattern('TraderReady'))
    #await sub.unsubscribe('InRedis:1')
    #await tsk
    sub.close()
    pub.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    loop.run_forever()
