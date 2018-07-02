import json
import random
from datetime import datetime
from multiprocessing import Pool

import numpy as np
import asyncio
import aioredis
from Agent import Agent
from TradingData import TradinData

loop = asyncio.get_event_loop()

STOPWORD = 'STOP'

class TradingBot(object):
    """
    Wir haben eine Population aus Agenten erzeugt
    Als nächstes müssen wir jeden Agenten mit den Daten, die wir geladen haben,   <traden> lassen
    """

    def initBot(self):
        print('initBot-Start')
        # lines = sys.stdin.readline()
        # print('argv[0]: '+lines[0])
        #tsk = asyncio.ensure_future(self.(ch1))
        print('initBot: inputData '+str(self.inputData))
        self.populationSize = int(self.inputData['agentenAnzahl']) #int(self.data.agentenAnzahl) #int(sys.argv[1])  #int(lines[0]) #
        self.generationAnzahl = int(self.inputData['generationAnzahl']) #int(self.data.generationAnzahl) #int(sys.argv[2])   #int(lines[1]) #3

        self.data = TradinData().data
        print('initBot: inputData '+str(self.inputData))

        for x in range(0, self.populationSize):
            self.population.append(Agent(self.data)) #, self.inputData

        print('Size: ', self.populationSize, len(self.population))
        self.startBot()

    async def publishInRedis(self, chanel, msg):
        await self.initRedis()
        #tsk = asyncio.ensure_future(self.initRedis(), loop=loop)
        print('publishInRedis')
        async def publish(chanel):
            self.pub = await aioredis.create_redis('redis://localhost')
            '''while not tsk.done():
    # wait for clients to subscribe
    while True:
        subs = await pub.pubsub_numsub('TraderReady')
        if subs[b'TraderReady'] == 1:
            break
        await asyncio.sleep(0, loop=loop)
    # publish some messages
    for msg in ['one', 'two', 'three']:
        await pub.publish('TraderReadys', msg)'''
            # send stop word
            await self.pub.publish('TraderReadys', STOPWORD)
            await self.pub.publish(chanel, msg)#'Result is in Redis'
            #pub.close()
            #await pub.wait_closed()
        '''if loop.is_running():
            print('loop.is_running')
            return None
        else:
            return loop.run_until_complete(asyncio.gather(publish(), tsk, loop=loop))'''

    async def initRedis(self):
        self.pool = await aioredis.create_pool('redis://localhost', minsize=5, maxsize=10)

        async def reader(channel):
            while await channel.wait_message():
                msg = await channel.get(encoding='utf-8')
                print('inputData initRedis', self.inputData)

                if channel.name == b'TraderReady':
                    self.inputData = json.loads(msg)
                    return self.inputData

                # ... process message ...
                print("message cc TraderReady in {}: {}".format(channel.name, msg))
                print('inputData initRedis', self.inputData)
                if msg == STOPWORD:
                    return

        '''with await pool as conn:
            await conn.execute_pubsub('subscribe', 'TraderReady')
            channel = conn.pubsub_channels['TraderReady']
            await reader(channel)  # wait for reader to complete
           # await conn.execute_pubsub('unsubscribe', 'TraderReady:1')
    '''
        # Explicit connection usage
        conn = await self.pool.acquire()

        try:
            await conn.execute_pubsub('subscribe', 'TraderReady')
            channel = conn.pubsub_channels['TraderReady']
            print('initRedis conn')
            await reader(channel)  # wait for reader to complete
            await conn.execute_pubsub('unsubscribe', 'TraderReady')

        finally:
            'returns used connection back into pool.'
            self.pool.release(conn)
            self.initBot()

        #pool.close()
        #await pool.wait_closed()
        print('initRedis conn closed')

    '''def initRedis(self):

        sub = yield from aioredis.create_redis(('localhost', 6379))
        res = yield from sub.psubscribe("enibar-*")
        subscriber = res[0]

        loop = asyncio.get_event_loop()

        # Create Redis connection
        transport, protocol = yield from loop.create_connection(
            asyncio_redis.RedisProtocol, 'localhost', 6379)
        # Set a key
        yield from protocol.set('my_key', 'my_value')

        # Get a key
        result = yield from protocol.get('my_key')
        print(result)

        # Close transport when finished.
        transport.close()

        # Create connection
        self.connection = yield from asyncio_redis.Connection.create(host='localhost', port=6379)

        # Create subscriber.
        self.subscriber = yield from self.connection.start_subscribe()

        # Subscribe to channel.
        yield from self.subscriber.subscribe(['TraderReady'])

        # Inside a while loop, wait for incoming events.
        while True:
            reply = yield from self.subscriber.next_published()
            print('Received: ', repr(reply.value), 'TraderReady', reply.channel)

        # When finished, close the connection.
        #self.connection.close()'''

    def __init__(self):

        '''self.redis = redis.StrictRedis(host='localhost', port='6379')
        self.pubsub = self.redis.pubsub()

        self.redis.publish('TraderReady', 'START')
        self.pubsub.subscribe('TraderReady')'''
        #self.pubsub.subscribe("InRedis")
        print('__init_')
        self.inputData = {}
        self.populationSize = None
        self.generationAnzahl = None
        self.population = []
        self.data = None
        self.pool = None
        self.pub = asyncio.async(aioredis.create_redis('redis://localhost'))
        self.key = ''
        #loop.run_until_complete(asyncio.gather(self.initRedis(), tsk, loop=loop))
        #task = asyncio.ensure_future(self.publishInRedis())
        #task = loop.create_task(self.publishInRedis())
        loop.run_until_complete(self.publishInRedis('TraderReady', 'Trader is ready'))
        #loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(loop), return_exceptions=True))

        print('__init__')
        '''loop = asyncio.get_event_loop()
        tsk = asyncio.ensure_future(self.initRedis(), loop=loop)
        loop.run_until_complete(asyncio.gather(self.publishInRedis(), tsk, loop=loop))'''
        #self.subscriber = RedisSubscriber.RedisSubscriber()
        #self.subscriber.connect()
        #asyncio.ensure_future(self.subscriber.subscribe('TraderReady:1'))
        #self.subscribe.subscribe('chan:1')


        '''while True:
            reply = yield from self.subscriber.next_published()
            print('Received: ', repr(reply.value), 'on channel', reply.channel)'''
        print('inputData __init__', self.inputData)
        if self.inputData != {}:
            print('MSG: ' + self.inputData.decode("utf-8"))

        #channel, reply = await self.sub.listen()
        #for message in self.pubsub.listen():
        #self.inputData = '{"agentenAnzahl":"1000","generationAnzahl":"3","buy_range_von":"1","buy_range_bis":"1000","sell_range_von":"1","sell_range_bis":"1000","buy_stoplos_von":"1","buy_stoplos_bis":"1000","sell_stoplos_von":"1","sell_stoplos_bis":"1000","email_input":"uu4axvkbuwdxcapx@ethereal.email"}'
        if type(self.inputData) == int:
            print('message: '+str(self.inputData))
        else:
            print('message: '+self.inputData.decode("utf-8"))
            self.inputData = json.loads(self.inputData.decode("utf-8"))
            print('TradingBot __init: inputData ' + str(self.inputData))
            self.key = 'Output:{}/{}/{}/{}/{}/{}/{}/{}/{}/{}'.format(self.inputData['agentenAnzahl'],self.inputData['generationAnzahl'],
                                                                      self.inputData['buy_range_von'],
                                                                      self.inputData['buy_range_bis'],
                                                                      self.inputData['sell_range_von'],
                                                                      self.inputData['sell_range_bis'],
                                                                      self.inputData['buy_stoplos_von'],
                                                                      self.inputData['buy_stoplos_bis'],
                                                                      self.inputData['sell_stoplos_von'],
                                                                      self.inputData['sell_stoplos_bis'])
            #if( self.key in self.redis.keys())
            print('self.key: '+self.key)
            #for key in self.redis.scan_iter():
                #if( self.key in key.decode('ASCII')):
                #print('key.decode'+key.decode('ASCII'), self.key in key.decode('ASCII'))
            #print('Keys: '+ ', '.join(self.redis.keys()))
            print('agentenAnzahl: ', self.inputData['agentenAnzahl'])
            print('buy_range_von: ', self.inputData['buy_range_von'])

            self.initBot()


    def startBot(self):
        outputStr=''
        print('Start Bot: ')
        self.start = datetime.now()
        dateiName = str(self.start.microsecond)
        print('dateiName: ', dateiName)
        for y in range(0, self.generationAnzahl):
            # usdGewinne=self.fitnessFkt()
            outputStr += '{} {}\n'.format('time start: ', str(self.start))
            outputStr += '{} {}\n'.format('time start: ', str(self.start))
            print("current generation: ", y)
            outputStr += 'current generation is {}\n'.format(y)
            print('agents vor fitnessFunction: ' + str(len(self.population)))
            self.fitnessFunction()

            if y == self.generationAnzahl-1:
                print('Hier is '+str(y))
                agents = sorted(self.population, key=lambda x: x.portfolio['USD'], reverse=True)
                print('agents: '+str(agents[0].genotype.chromosome))
                holdings = (1000 / float(self.data[0])) * float(self.data[-1])
                outputStr += 'Die Tradesanzahl von der besten Strategie: {}\n'.format(agents[0].tradesNum)

                outputStr += 'Die Beste Strategie ist zu kaufen, auf einen Anstieg von : {} % zu warten und dann bei einem Abfall von {}% zu verkaufen\n'.format(agents[0].genotype.verkaufProzent, agents[0].genotype.einkaufProzent)
                outputStr += 'sollte der Preis unter {:.2f} % von Einkaufswert fallen dann verkaufe\n'.format(agents[0].genotype.stoplossVerkauf * agents[0].genotype.verkaufProzent)
                outputStr += ' Oder sollte er {:.2f} % über den Verkaufswert steigen dann kaufe\n'.format(agents[0].genotype.stoplossEinkauf * agents[0].genotype.einkaufProzent)

                '''for x in agents:
                    fo.write(" (%(usd).2lf %(einkaufProzent).2lf %(verkaufProzent).2lf %(stoplossEinkauf).2lf %(stoplossVerkauf).2lf "
                             "%(tradesNum).2lf %(gezahlt).2lf)\n" % {"usd": x.portfolio['USD'], "einkaufProzent": x.genotype.einkaufProzent,
                            "verkaufProzent":x.genotype.verkaufProzent, "stoplossEinkauf":  x.genotype.stoplossEinkauf ,
                             "stoplossVerkauf": x.genotype.stoplossVerkauf, "tradesNum": x.tradesNum, "gezahlt":  x.gezahlt})
                    '''
                outputStr += 'Hold {} \n'.format(holdings)
                print('outputStr: '+outputStr)

                outputStr += 'The best strategy is {} % better than holding\n'.format(((agents[0].portfolio['USD'] / holdings * 100) - 100 ))
                outputStr += 'Entire job took:{} \n'.format(str(datetime.now() - self.start))

                asyncio.async(self.pool.execute('set', self.key+'/'+dateiName, outputStr))
                print(asyncio.async(self.pool.execute('get', self.key+'/'+dateiName)))

                #self.redis.set(self.key+'/'+dateiName, outputStr)
                #self.pub.publish('InRedis', 'Result is in Redis')
                value = asyncio.async(self.pool.execute('get', dateiName))

                print('value: ', value)

                break
            else:
                self.population = self.kreuzung()
                print('Nachdem Kreuzen: ' + str(self.population))

            # print("usdGewinne: ",usdGewinne)

        # print(len(self.population))
        # print("Fitness fkt fertig!!")



    def fitnessFunction(self):
        t1 = datetime.now()
        usdGewinne = []
        print("Testing Strategies....")
        self.threader()
        print("Pool took: ", datetime.now() - t1)

    def worker(self, agent):
        agent.startTrading()
        return agent



    def threader(self):
        """ Pool creates the pool of processes that controls the workers.
        parallelizing the execution of a function across multiple input values
        distributing the input data across processes(data paralallism)
        """
        p = Pool()
        print('Size in Pool: ', self.populationSize, len(self.population))
        print('Threader: ' + str(len(self.population)))
        result = p.map_async(self.worker, self.population) #p.map(self.worker, self.population)

        #print('Size: ', self.populationSize, result.ready())
        #print('Wainting ...')
        #print('result.get: ',result.get())

        p.close()
        #self.binFertig()
        if result.ready():
            if result.successful():
                self.population = result.get()
                print('Result: '+self.population)





    """
     2 Agenten auswählen, nach ihrer Wahrscheinlichkeit ausgewählt zu werden
    Diese beiden mit einer Wahrscheinlichkeit miteinander paaren
    Die Kinder falls Sie sich gepaart haben, werden einer neue Generation hinzugefügt un die Eltern sterben
    Sollten Sie sich nicht paaren, werden die Eltern in der neuen Generation hinzugefügt
    """

    """Random pairs or individuals are mated using a process of crossover, in which new individuals inherit genes from
     parent. In addition offspring(Nachwuchs) undergo random mutation, in which genes change by a random amount
   """
    def kreuzung(self):
        print("Kreuzen....")
        print('agent0 hat ' + str(self.population[0].portfolio['USD']) + '$ und '+str(self.population[0].portfolio['BTC'])+'btc')
        newGeneration = []
        maxUsdSum = int(sum(map(lambda x: x.portfolio['USD'], self.population)))
        print('maxUsdSum: '+str(maxUsdSum))
        for x in range(int(self.populationSize / 2)):
            a = self.selectOne(maxUsdSum)
            print('Kreuzng a: '+str(a.genotype.chromosome))
            aChromosome = a.genotype.chromosome
            print('Kreuzung aChromosome: '+str(aChromosome))
            b = self.selectOne(maxUsdSum)
            bChromosome = b.genotype.chromosome

            obPaart = random.uniform(0, 1)
            # Es wird zu 60% gepaart
            if obPaart <= 0.6:
                a, b = self.paarung(a, b)
            else:
                a = Agent(self.data, aChromosome)
                b = Agent(self.data, bChromosome)

            newGeneration.append(a)
            newGeneration.append(b)
        print('newGeneration = ' + str(newGeneration))
        return newGeneration

    def filppeBit(self, zeichen):
        if zeichen == '1':
            return '0'
        else:
            return '1'

    def mutation(self, chromosome):
        # print("chro: ",chromosome)
        res = list(chromosome)
        max = 1000
        for i in range(len(chromosome)):
            # Zur Wahrscheinlichkeit von 1/100 flippen wir
            if (np.random.randint(1, max) == 1):
                res[i] = self.filppeBit(chromosome[i])
        return ''.join(res)

    def paarung(self, p1, p2):
        newGeneration = []
        counter = 0
        mutiertListP1 = []
        mutiertListP2 = []
        # x*10 um die bin() benutzen zu können
        # 'ob0100101' in binP1
        #print('P1: Genotype '+str(p1.genotype.chromosome))
        binP1 = [bin(int(x * 10))[2:] for x in p1.genotype.chromosome]
        maxLen = len(max(binP1, key=len)) if binP1 else 0
        # print("binP1: ", [ len(x) for x in binP1])
        binP2 = [bin(int(x * 10))[2:] for x in p2.genotype.chromosome]
        maxLen2 = len(max(binP2, key=len))if binP2 else 0
        if maxLen2 > maxLen:
            maxLen = maxLen2

        binP1 = [str(x).zfill(maxLen) for x in binP1]
        binP2 = [str(x).zfill(maxLen) for x in binP2]
        # print("binP2: ", [ len(x) for x in binP2])
        for x in binP1:
            n = len(x)
            # print("n: ", n)
            schnittStelle = np.random.randint(1, n - 1)
            for y in binP2[counter:]:
                up1 = x[schnittStelle:]
                ux = y[schnittStelle:]
                uy = up1
                break
            counter += 1
            # Tausche
            # print(len(self.mutation( x[0:schnittStelle] + uy )))
            # wert/10 um auf die initiale wert zu kommen
            xMuttiert = int(self.mutation(x[0:schnittStelle] + uy), 2) / 10
            mutiertListP1.append(xMuttiert)

            yMuttiert = int(self.mutation(y[0:schnittStelle] + ux), 2) / 10
            mutiertListP2.append(yMuttiert)
        a = Agent(self.data, mutiertListP1)
        b = Agent(self.data, mutiertListP2)

        return a , b

    def selectOne(self, maxValue):
        pick = random.uniform(0, maxValue)
        current = 0
        counter = 0
        for c in self.population:
            current += float(c.portfolio['USD'])
            if pick <= current:
                print('SelectOne: '+str(pick)+'='+str(counter)+'->'+str(self.population[counter].genotype.chromosome))
                return self.population[counter]
            counter += 1


if __name__ == '__main__':
    print("hello")
    TradingBot()
    #start.initBot()
    #fo = open("out.txt", "a+",  encoding='utf-8')
    #fo.write("_Salwa");
    """
    # with 10 workers and 20 tasks, with each task being .5 seconds, then the completed job
    # is ~1 second using threading. Normally 20 tasks with .5 seconds each would take 10 seconds.
    print('Entire job took:', time.time() - start)
"""