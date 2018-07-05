from datetime import datetime
from Agent import Agent
from multiprocessing import Process, Queue, Pool, Manager
import os
import random
import numpy as np
from TradingData import TradinData
import asyncio
import redis
import json

class TradingBot(object):
    """
    Wir haben eine Population aus Agenten erzeugt
    Als nächstes müssen wir jeden Agenten mit den Daten, die wir geladen haben,   <traden> lassen
    """
    def initBot(self, inputData):
        print('InitBot->:'+ str(inputData))
        # lines = sys.stdin.readline()
        # print('argv[0]: '+lines[0])
        self.populationSize = int(inputData['agentenAnzahl']) #int(self.data.agentenAnzahl) #int(sys.argv[1])  #int(lines[0]) #
        self.generationAnzahl = int(inputData['generationAnzahl']) #int(self.data.generationAnzahl) #int(sys.argv[2])   #int(lines[1]) #3
        self.population = []
        self.data = TradinData().data
        self.inputData = inputData

        for x in range(0, self.populationSize):
            self.population.append(Agent(self.data, self.inputData))
        print('populationSize: '+str(self.populationSize)+'\tgenerationAnzahl:'+str(self.generationAnzahl))
        self.startBot()


    def __init__(self):

        self.redis =redis.StrictRedis( host='localhost',port='6379')
        p = self.redis.pubsub()
        self.redis.set('foo','bar')
        value= self.redis.get('foo')
        print(value)
        self.redis.publish('Test', 'START')
        p.subscribe('TraderReady')
        for message in p.listen():
            self.inputData =message['data']
            if( type(self.inputData) == int ):
                print('message: '+ str(self.inputData))
            else:
                print('message: '+ self.inputData.decode("utf-8") )
                inputData = json.loads(self.inputData.decode("utf-8"))
                print('agentenAnzahl: ', str(inputData))
                self.initBot(inputData)

    def startBot(self):
        #wechselt das Verzeichnis damit man auf die Outputdateien zugreifen kann.
        #toDirectory= os.getcwd() if ('output' in os.getcwd() ) else os.getcwd() + r'\output'
        #os.chdir(toDirectory)
        print('Start Bot: ',os.getcwd())
        #i= int(os.listdir(os.getcwd())[-1].split('.txt')[0][3:]) + 1
        outputStr=''
        #Open a File
        self.start = datetime.now()
        dateiName = 'Output:'+str(self.start.microsecond)
        print('dateiName: ', dateiName)

        #fo= open(dateiName,"w")
        for y in range(0, self.generationAnzahl):
            #outputStr += '{} {}\n'.format('time start: ', str(datetime.now() - self.start))

            #outputStr += 'current generation is {}\n'.format(y)
            print("current generation: ", y)
            print('{} {}\n'.format('Time start: ', str(datetime.now() - self.start)))
            self.fitnessFunction()

            if y == self.generationAnzahl-1:
                agents = sorted(self.population, key=lambda x: x.portfolio['USD'], reverse=True)
                holdings = (1000 / float(self.data[0])) * float(self.data[-1])

                #print("  USD, einkaufProzent, verkaufProzent, stoplossEinkauf, stoplossVerkauf")

                outputStr += 'Die Tradesanzahl von der besten Strategie: {}\n'.format(agents[0].tradesNum)
                #print("Die Tradesanzahl von der besten Strategie is ", agents[0].tradesNum)
                outputStr += 'Die Beste Strategie ist zu kaufen, auf einen Anstieg von : {} % zu warten und dann bei einem Abfall von {}% zu verkaufen\n'.format(agents[0].genotype.verkaufProzent, agents[0].genotype.einkaufProzent)




                #print("Die Beste Strategie ist zu kaufen, auf einen Anstieg von ", agents[0].genotype.verkaufProzent,"% zu warten und dann bei einem Abfall von ", agents[0].genotype.einkaufProzent, "% zu verkaufen")
                '''fo.write("Die Beste Strategie ist zu kaufen, auf einen Anstieg von %(verkaufProzent).2lf %% zu warten und dann bei einem Abfall von %(einkaufProzent).2lf %% zu verkaufen\n"%
                         {"verkaufProzent":agents[0].genotype.verkaufProzent, "einkaufProzent":agents[0].genotype.einkaufProzent})
                '''
                outputStr += 'sollte der Preis unter {:.2f} % von Einkaufswert fallen dann verkaufe\n'.format(agents[0].genotype.stoplossVerkauf * agents[0].genotype.verkaufProzent)

                outputStr += ' Oder sollte er {:.2f} % über den Verkaufswert steigen dann kaufe\n'.format(agents[0].genotype.stoplossEinkauf * agents[0].genotype.einkaufProzent)
                outputStr += 'Hold {} \n'.format(holdings)
                outputStr += 'The best strategy is {} % better than holding\n'.format(((agents[0].portfolio['USD'] / holdings * 100) - 100))
                outputStr += 'Entire job took:{} \n'.format(str(datetime.now() - self.start))

                self.redis.set(dateiName, outputStr)
                self.redis.publish('InRedis', outputStr)
                break
            else:
                self.population = self.kreuzung()

            # print("usdGewinne: ",usdGewinne)

        # print(len(self.population))
        # print("Fitness fkt fertig!!")
        print('outoputStr: '+outputStr)



    def fitnessFunction(self):
        t1 = datetime.now()
        usdGewinne = []
        print("Testing strategies....")
        self.threader()
        #print("Pool took: ", datetime.now() - t1)

    def worker(self, agent):
        agent.startTrading()
        return agent

    def threader(self):
        """ Pool creates the pool of processes that controls the workers.
        parallelizing the execution of a function across multiple input values
        distributing the input data across processes(data paralallism)
        """
        async def threader_async():
            p = Pool()
            res = p.map(self.worker, self.population)
            self.population = res[:]
            p.close()
            p.join()

        asyncio.async(threader_async())



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
        newGeneration = []
        max = int(sum(map(lambda x: x.portfolio['USD'], self.population)))

        for x in range(int(self.populationSize / 2)):
            a = self.selectOne(max)
            aChromosome = a.genotype.chromosome
            b = self.selectOne(max)
            bChromosome = b.genotype.chromosome

            obPaart = random.uniform(0, 1)
            # Es wird zu 60% gepaart
            if obPaart <= 0.6:
                (a, b) = self.paarung(a, b)
            else:
                a = Agent(self.data, self.inputData, aChromosome)
                b = Agent(self.data, self.inputData, bChromosome)

            newGeneration.append(a)
            newGeneration.append(b)

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
        binP1 = [bin(int(x * 10))[2:] for x in p1.genotype.chromosome]
        maxLen = len(max(binP1, key=len))
        # print("binP1: ", [ len(x) for x in binP1])
        binP2 = [bin(int(x * 10))[2:] for x in p2.genotype.chromosome]
        maxLen2 = len(max(binP2, key=len))
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
        a = Agent(self.data, self.inputData, mutiertListP1)
        b = Agent(self.data, self.inputData, mutiertListP2)

        return (a, b)


    def selectOne(self, max):
        pick = random.uniform(0, max)
        current = 0
        counter = 0
        for c in self.population:
            current += float(c.portfolio['USD'])
            if pick <= current:
                return self.population[counter]
            counter += 1


if __name__ == '__main__':
    #print("hello")
    TradingBot()
    #fo = open("out.txt", "a+",  encoding='utf-8')
    #fo.write("_Salwa");
    """
    # with 10 workers and 20 tasks, with each task being .5 seconds, then the completed job
    # is ~1 second using threading. Normally 20 tasks with .5 seconds each would take 10 seconds.
    print('Entire job took:', time.time() - start)
"""