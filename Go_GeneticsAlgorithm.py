# -*- coding: utf-8 -*-
"""
Created on Wed May  2 18:39:53 2012

@author: gofrendi
"""
from Go_Random import Go_Random
from randomFunction import randomFunction

class Go_GeneticsAlgorithm(object):
    
    def __init__(self):
        self.mutationRate = 50
        self.crossoverRate = 30
        self.elitismRate = 10
        self.newRate = 10
        self.maxEpoch = 100
        self.populationSize = 100
        self.generation = [] #list
        self.random = Go_Random(randomFunction)
        self.chromosomeLength = 50
        self.minCodon = 0
        self.maxCodon = 1
        self.calculatedFitness = {}
    
    def __str__(self):
        string = ''
        for i in xrange(len(self.generation)):
            string+= '\nGeneration %d\n' % i
            for j in xrange(self.populationSize):
                fitness = str(j)
                string+= 'fitness #%s : %5.3f, ' % (fitness.rjust(3), self.generation[i][j]['fitness'])
            string += '\n'
        return string    
    
    
    def __currentGenerationIndex(self):
        return len(self.generation)-1
    
    def _mutation(self, chromosome): 
        #return new chromosome        
        random = int(round(self.random.get(0,self.chromosomeLength-1)))
        newCodon = self.minCodon+((chromosome[random]-self.minCodon+1) % (self.maxCodon+1-self.minCodon))       
        chromosome[random] = newCodon
        return chromosome
    
    def _crossover(self, chromosome1, chromosome2): 
        #return new chromosome
        random = int(round(self.random.get(0,self.chromosomeLength-1)))
        segment1 = chromosome1[0:random]
        segment2 = chromosome2[random:self.chromosomeLength]
        chromosome = segment1+segment2
        return chromosome
    
    def _new(self): 
        #return new chromosome
        chromosome = []
        i=0
        while i< self.chromosomeLength:
            random = int(round(self.random.get(self.minCodon,self.maxCodon)))
            chromosome.append(random);
            i+=1
        return chromosome
    
    def _pick(self, index=None): 
        #return any chromosome from current generation
        currentGenerationIndex = self.__currentGenerationIndex()
        currentGeneration = self.generation[currentGenerationIndex]
        if index!=None:
            return currentGeneration[index]['chromosome'][:]
        else:
            maxCumSum = float(currentGeneration[self.populationSize-1]['cumsum'])           
            random = float(self.random.get(0,maxCumSum))
            chromosome = None
            i=0
            while random > currentGeneration[i]['cumsum'] and i<len(currentGeneration)-1:
                i += 1
            chromosome = currentGeneration[i]['chromosome'][:]
            return chromosome
    
    def _fitnessFunction(self, chromosome):
        #you surely need to override this        
        return sum(chromosome)
        
    def _makeNextGeneration(self):        
        newGeneration = []
        #the ratio below are related to the decision created                 
        elitismLimit = float(self.elitismRate)
        mutationLimit = elitismLimit+float(self.mutationRate)
        crossoverLimit = mutationLimit+float(self.crossoverRate)
        allLimit = crossoverLimit+float(self.newRate)
        elitismRatio = elitismLimit/allLimit
        mutationRatio = mutationLimit/allLimit
        crossoverRatio = crossoverLimit/allLimit
        
        for i in xrange(self.populationSize):
            newChromosome = []
            
            if(self.__currentGenerationIndex()==-1):
                newChromosome = self._new()
            else:
                ratio=float(i)/float(self.populationSize)
                newChromosome = []
                if ratio <= elitismRatio:
                    newChromosome = self._pick(i)
                elif ratio <= mutationRatio:
                    newChromosome = self._mutation(self._pick())
                elif ratio <= crossoverRatio:
                    newChromosome = self._crossover(self._pick(), self._pick())
                else:
                    newChromosome = self._new()
                    
            
            #calculate fitness if needed or take from self.calculatedFitness
            #if calculation has been performed before
            fitness=0   
            chromosomeKey = ' '.join(map(str,newChromosome))
            if not(chromosomeKey in self.calculatedFitness): 
                fitness = self._fitnessFunction(newChromosome) #calculate...
                self.calculatedFitness[chromosomeKey] = fitness #and save
            else:
                fitness = self.calculatedFitness[chromosomeKey] #take from calculated
            
            #new Individu
            newIndividu = {'chromosome' : newChromosome, 
                           'fitness' : fitness,
                           'cumsum' : 0}
            newGeneration.append(newIndividu)
                
        
        
        #sort the new generation based on their fitness      
        newGeneration_dec = map(lambda x: (x["fitness"],x), newGeneration)
        newGeneration_dec.sort(reverse=True) 
        newGeneration = map(lambda x: x[1],newGeneration_dec)
         
        #calculate cumsum
        cumsum=0
        for i in xrange(self.populationSize):
            cumsum += newGeneration[i]['fitness']
            newGeneration[i]['cumsum'] = cumsum
        self.generation.append(newGeneration)
        self._printProgress()
    
    def _printProgress(self):
        currentGenerationIndex = self.__currentGenerationIndex()
        currentGeneration = self.generation[currentGenerationIndex]
        bestFitness = currentGeneration[0]['fitness']
        
        print('Generation %d, best fitness : %5.5f'%(currentGenerationIndex, bestFitness))
        
    def train(self):
        i=0
        while i<self.maxEpoch: 
            self._makeNextGeneration()
            i+=1

if __name__ == '__main__':
    ga = Go_GeneticsAlgorithm()
    ga.train()
    #print(ga)