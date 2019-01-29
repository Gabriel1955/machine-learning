'''
https://aydanomachado.com/mlclass/02_Optimization.php?
phi1=90&theta1=90&phi2=90&theta2=90&phi3=90&theta3=90&dev_key=Simple%20Agent*

'''
from random import *
import copy
import random
import requests
import json
import threading
import numpy as np
import numpy.random



dev_key = "Os ifzinhos"
size_population = 20
precision = 1

class Chromosome:
    phi1 = 0
    theta1 =0 
    phi2 = 0
    theta2 = 0
    phi3 = 0
    theta3 = 0

    score = 0

    def __init__(self):
         self.phi1 = getRamdomGene()
         self.theta1 = getRamdomGene()
         self.phi2 = getRamdomGene()
         self.theta2 = getRamdomGene()
         self.phi3 = getRamdomGene()
         self.theta3 = getRamdomGene()
         self.score = 0

def getRamdomGene():
    aux_precision = 10**precision
    gene = randint(0,359*aux_precision)
    return gene/aux_precision
    
def createPopulation():
    population = []
    i = 0
    while i < size_population*2:
        population.append(Chromosome())
        i += 1
    return population
def toEvaluatePopulation(population, best):
    i = 0
    threads = []
    #print("to")
    while i < len(population):
        threads.insert(i,threading.Thread(target=getScore,args=(population[i],i)))
        threads[i].start()
        i += 1
    #print("to 2 ")
    while(threadsIsAlive(threads)):
        pass
    #print("to 3 ")
        
    i = 0
    while i <len(population):
        if population[i].score > best.score:
            best = population[i]
        i +=1
    #print("to 4 ")        
    return best

def threadsIsAlive(threads):
    for t in threads:
        if t.isAlive():
            return True
    return False

def getScore(chromosome,i):
    params = {"phi1": chromosome.phi1, "theta1": chromosome.theta1,
              "phi2": chromosome.phi2, "theta2": chromosome.theta2,
              "phi3": chromosome.phi3, "theta3": chromosome.theta3, "dev_key": dev_key }
    URL = "https://aydanomachado.com/mlclass/02_Optimization.php"
    r = requests.post(url=URL, data=params)
    gain = json.loads(r.text)['gain']
    
    print("get score " +str(i)+ " get: "+str(gain)+"\n")
    
    chromosome.score = gain
    return gain

def selectionPopulation(population):
    population.sort(key=lambda a: a.score, reverse=True)
    return population[0:size_population]

def mutationPopulation(population):
    news_chromosome = []
    for p in population:
        news_chromosome.append(copy.copy(p))

    i = 0
    while i < len(news_chromosome):
        for index in random.sample(range(6), randint(0,4)):
            new_value = getRamdomGene()
        
            if index == 0:
                news_chromosome[i].phi1 = new_value
            elif  index == 1:
                news_chromosome[i].theta1 = new_value
            elif index == 2:
                news_chromosome[i].phi2 = new_value
            elif index == 3:
                news_chromosome[i].theta2 = new_value
            elif index == 4:
                news_chromosome[i].phi3 = new_value
            elif index == 5:
                news_chromosome[i].theta3 = new_value
            else :
                print("eero")
        i += 1
    return news_chromosome
    
def printChromosome(chromosome):
    print("phi1 "+str(chromosome.phi1))
    print("theta1 "+str(chromosome.theta1))
    print("phi2 "+str(chromosome.phi2))
    print("theta2 "+str(chromosome.theta2))
    print("phi3 "+str(chromosome.phi3))
    print("theta3 "+str(chromosome.theta3))
    print("score "+str(chromosome.score))
    print("")
    
def main():
    #getScore(Chromosome())
    #print(random.sample(range(6), randint(1,6)))
    
    best_chromosome = Chromosome()
    population_global = createPopulation()
    best_chromosome = toEvaluatePopulation(population_global, best_chromosome)
    i = 0
    aux_precision = 0
    while 1:
        population_global = selectionPopulation(population_global)
        mutation = mutationPopulation(population_global)

        bestScore = best_chromosome.score

        best_chromosome = toEvaluatePopulation(mutation, best_chromosome)

        if bestScore == best_chromosome.score:
            aux_precision +=1
            if aux_precision > 20:
                aux_precision = 0
                global precision
                precision +=1
                if precision > 20:
                    precision = 20
                    
        elif bestScore < best_chromosome.score:
            printChromosome(best_chromosome)
        
        population_global += mutation        
        
        i+=1
    
    
    









    return 0
if __name__ == "__main__":
    main()
