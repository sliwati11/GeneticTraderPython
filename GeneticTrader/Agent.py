#!/usr/bin/env python
# -*- coding: utf8 -*-
from Genotype import Genotype

"""
Die Aufgabe des Agenten: Er kauft und verkauft unter bestimmten Bedingungen , diese nennen sein Verhalten
Diese Bedingungen sind in seinen Genen codiert, welche man in Genotype findet
Eine bestimmte Ausprägung der Gene nennt man Genotype
Im Portfolio befindet sich das Komplette Guthaben
Er bekommt vom tradingBot eine Referenz auf eine Liste alle Trades, auf diese Liste soll er seine Strategie anwenden
Am Ende nachdem er seine Strategie angewendet hat, schauen wir wie viel Geld er hat.
Die Menge des Geldes am ende des Tradens ist der Wert, den die Fitnessfonktion zur Evaluierung der Fitness des Agenten
"""
class Agent(object):

    def __init__(self, handleData, inputData ,chromosomeList=None): #inputData=None

        self.lastPrice = 0
        self.tradesNum = 0
        self.gezahlt = 0
        self.fees = 0.01
        self.handleData = handleData
        self.inputData = inputData
        #self.inputData = inputData.copy()

        #print('In Agent: '+str(self.inputData))

        if chromosomeList is None:
            print('Agent inputData:' + str(self.inputData))
            self.genotype = Genotype(self.inputData) #self.inputData

        else:
            print('Agent inputData:'+str(self.inputData))
            self.genotype = Genotype(self.inputData, chromosomeList)

        self.alwaysInit(self.handleData)

    """Der agent wird immer so initialisiert"""
    def alwaysInit(self, data):
        self.portfolio = {'USD': 100, 'BTC': 0}
        self.data = data
        self.lastPrice = float(self.handleData[0])
        # print( self.lastPrice )
        """Kaufe alles"""
        self.portfolio['BTC'] = self.portfolio['USD'] / self.lastPrice
        self.portfolio['USD'] = 0
        # print("BTC ", self.portfolio['BTC'])
        # print("USD ", self.portfolio['USD'])


    #Fitness Fkt
    def startTrading(self):
        #print("#Start Trading")
        for actPrice in map(float, self.handleData):
            #print("lastPrice: ", self.lastPrice)
            diff = actPrice - self.lastPrice
            diff_in_prozent = diff / self.lastPrice * 100
            if (self.portfolio['USD'] != 0):
                #Ich habe USD
                #Wenn der einkaufspreis steigt um ein gewissen EinkaufProzent
                if diff_in_prozent <= -1*self.genotype.einkaufProzent or diff_in_prozent > self.genotype.stoplossEinkauf:
                    self.kaufe(actPrice)
            else:#Ich habe BTC
                if diff_in_prozent >= self.genotype.verkaufProzent or diff_in_prozent <= -1 * self.genotype.stoplossVerkauf:
                    self.verkaufe(actPrice)

        if self.portfolio['USD'] == 0:
            self.verkaufe(actPrice)
        ''' mit weniger als 15 Trades soll er das Geld verlieren'''
        if self.tradesNum < 15:
            self.portfolio['USD'] = 0

        #print("Trades number:",self.tradesNum," Finisch Trading")




    def kaufe(self, actPreis):

            self.portfolio['BTC']= self.portfolio['USD'] / actPreis - self.fees * self.portfolio['USD'] / actPreis
            self.paid= self.fees * self.portfolio['USD'] / actPreis
            self.portfolio['USD'] = 0
            self.lastPrice= actPreis
            self.tradesNum +=1
            #print("rest: ", self.portfolio['USD'])

    def verkaufe(self, actPreis):

            #Verkaufe alles
            self.portfolio['USD'] = actPreis * self.portfolio['BTC'] - self.fees * actPreis * self.portfolio['BTC']
            self.gezahlt += self.fees * actPreis * self.portfolio['BTC']
            self.portfolio['BTC']= 0
            self.lastPrice = actPreis
            self.tradesNum += 1
            #print("verkauft")







