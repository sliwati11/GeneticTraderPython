import csv
import os
from datetime import datetime
import urllib.request


class TradingData(object):

    def __init__(self, inputData):
        print("load Trading Data")
        self.inputData = inputData
        #self.loadOnline()

        self.data = self.loadOnline()

    def loadDataOld(self):
        lowHigh = []

        files = ["Data/Bitcoincharts _ Charts_last5_1.csv",
                "Data/Bitcoincharts _ Charts_last5_2.csv",
                "Data/Bitcoincharts _ Charts_last5_3.csv",
                "Data/Bitcoincharts _ Charts_last5_4.csv",
                "Data/Bitcoincharts _ Charts_last5_5.csv"]

        file = "Data/Bitcoincharts _ Charts_last5_1.csv"
        start= datetime.now()
        print('read files starts\n')
        for file in files:
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    lowHigh.append(row['Open'])
        print('reading took '+str(datetime.now() - start) + ' ms')
        print("Load Trading Data is ready!")

        return lowHigh

    def loadData(self):
        print("Load new Data!!\n")
        #print('getcwd ',os.getcwd())
        file= "/Users/salwa/PycharmProjects/GeneticTrader/Data/Bitcoincharts _ Charts_last5_1.csv"
        preis =[]
        i = 0
        with open(file, "r") as f:
            reader= csv.reader(f)
            for row in reader:
                i = i+1
                if(i % 50 == 0):
                    i=0
                    preis.append(row[1])

        print("Load Trading Data is ready!")
        return preis

    def loadOnline(self):
        lowHigh = []

        url1 = 'https://bitcoincharts.com/charts/chart.json?m='+str(self.inputData['m'])
        url2 = '&SubmitButton=Draw&r='+str(self.inputData['r'])
        url3 = '&i='+str(self.inputData['i'])
        url4 = '&c=1s=&e=&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&'
        url = url1 + url2 + url3 + url4
        print('url: '+url)
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        responseList = eval(response.read().decode('utf-8'))
        print('Response:', len(responseList))
        for row in responseList:
            lowHigh.append(row[1]) #for parameter Open

        return lowHigh



