import numpy as np

"""
  Der kodierte Vektor der Entscheidungsvariablen.
    Von Genotyp hängt , welche Tradingsstategie ein Agent bekommt
"""
class Genotype(object):

    def __init__(self, listechromosome= None):
        """Die Chromosome werden in eine Liste reingeschrieben, damit wir später die Liste einfach
            durchlaufen und die Choromosome miteinander kreuzen können.
        """
        self.chromosome = []
        '''Um wie viel Prozent muss der Preis steigen, damit wir einkaufen'''
        self.einkaufProzent = np.random.randint(0, 2000) / 10
        '''Um wie viel Prozent muss der Preis fallen, damit wir kaufen'''
        self.verkaufProzent = np.random.randint(0, 2000) / 10
        '''Um wie viel prozentuale Verlust muss ich kaufen wenn ich verkauft habe'''
        self.stoplossEinkauf = np.random.randint(0, 2000) / 10
        '''Um wie viel prozentuale Verlust muss ich verkaufen wenn ich gekauft habe.'''
        self.stoplossVerkauf = np.random.randint(0, 2000) / 10

        if listechromosome == None:
            self.chromosome.append(self.einkaufProzent)
            self.chromosome.append(self.verkaufProzent)
            self.chromosome.append(self.stoplossEinkauf)
            self.chromosome.append(self.stoplossVerkauf)
        else:
            self.chromosome= listechromosome



