from random import  randint
import random
import numpy as np



def selectOne( fitnessValues ):
    pick = random.uniform(0, 100)
    current = 0
    counter = 0
    for c in fitnessValues:
        current += float(c)
        if current >= pick:
            return counter
        counter +=1



def kreuzung( population, sizeofPopulation, fitnessValues ):
    newGeneration = []

    for x in range(int(sizeofPopulation / 2)):
        a = bin( population[selectOne(fitnessValues)] )[2:]
        b = bin( population[selectOne(fitnessValues)] )[2:]

        n = len(a)
        schnittStelle = np.random.randint(1, n - 1)
        ua = a[schnittStelle:]
        ub = b[schnittStelle:]

        aMuttiert= mutation(a[0:schnittStelle] + ub)
        bMuttiert= mutation(b[0:schnittStelle] + ua)
        #print(mutation(a[0:schnittStelle] + ub), mutation(b[0:schnittStelle] + ua))
        newGeneration.append( int(aMuttiert,2))
        newGeneration.append( int(bMuttiert, 2))

    print("newer: ",newGeneration)
    return newGeneration


def filppeBit(zeichen):
    if zeichen == '1':
        return '0'
    else:
        return '1'


def mutation( chromosome ):
    #print("chro: ",chromosome)
    res= list(chromosome)
    max = 1000
    for i in range(len(chromosome)):
        if( np.random.randint(1,max)== 1 ):
            print("Mutation")
            res[i] =filppeBit(chromosome[i])
    #print("Mutation : ", res)
    return ''.join(res)


