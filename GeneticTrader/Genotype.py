import numpy as np

"""
  Der kodierte Vektor der Entscheidungsvariablen.
    Von Genotyp hängt , welche Tradingsstategie ein Agent bekommt
"""
class Genotype(object):

    def __init__(self, inputData, listechromosome= None) :
        """Die Chromosome werden in eine Liste reingeschrieben, damit wir später die Liste einfach
            durchlaufen und die Choromosome miteinander kreuzen können.
        """
        self.chromosome = []

        # if len(inputData) == 11:

        # self.inputData = inputData
        print('Genotype inputData: '+str(inputData))

        if isinstance(inputData, dict):
            #print('inputData is not None' + str(type(inputData)) + str(inputData['buy_range_von']))


            '''Um wie viel Prozent muss der Preis steigen, damit wir einkaufen'''
            self.einkaufProzent = np.random.randint(int(inputData['buy_range_von'][0]),
                                                    int(inputData['buy_range_bis'])) / 10  #np.random.randint(0, 2000) / 10
            '''Um wie viel Prozent muss der Preis fallen, damit wir kaufen'''
            self.verkaufProzent = np.random.randint(int(inputData['buy_stoplos_von']),
                                                    int(inputData['buy_stoplos_bis'])) / 10  #np.random.randint(0, 2000) / 10

            '''Um wie viel prozentuale Verlust muss ich kaufen wenn ich verkauft habe'''
            self.stoplossEinkauf = np.random.randint(int(inputData['buy_stoplos_von']),
                                                     int(inputData['buy_stoplos_bis'])) / 10 #np.random.randint(0, 2000) / 10

            '''Um wie viel prozentuale Verlust muss ich verkaufen wenn ich gekauft habe.'''
            self.stoplossVerkauf = np.random.randint(int(inputData['sell_stoplos_von']),
                                                     int(inputData['sell_stoplos_bis'])) / 10 #np.random.randint(0, 2000) / 10


        if listechromosome is None:
            #print('listechromosome is None: ' + str(inputData))
            self.chromosome.append(self.einkaufProzent)
            self.chromosome.append(self.verkaufProzent)
            self.chromosome.append(self.stoplossEinkauf)
            self.chromosome.append(self.stoplossVerkauf)


        elif listechromosome:
            #print('Genotyp verkaufProzentB: ' + str(self.verkaufProzent))

            self.chromosome = listechromosome[:]
            #print('listechromosome is not None: ' + str(self.chromosome))




