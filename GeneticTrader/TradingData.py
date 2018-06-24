import csv
import os

class TradinData(object):

    def __init__(self):
        print("load Trading Data")
        self.data= self.loadData()

    def loadDataOld(self):
        lowHigh = []

        files= ["Data/Bitcoincharts _ Charts_last5_1.csv",
                "Data/Bitcoincharts _ Charts_last5_2.csv",
                "Data/Bitcoincharts _ Charts_last5_3.csv",
                "Data/Bitcoincharts _ Charts_last5_4.csv",
                "Data/Bitcoincharts _ Charts_last5_5.csv"]

        for file in files:
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    lowHigh.append(row['Open'])

        print("Load Trading Data is ready!")

        return lowHigh

    def loadData(self):
        print("Load new Data!!\n")
        print('getcwd ',os.getcwd())
        file= "/Users/salwa/PycharmProjects/GeneticTrader/Data/dataTest"
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

if __name__ == '__main__':

    trade = TradinData()
    print(trade.loadData()[-1])

