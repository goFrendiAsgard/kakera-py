# -*- coding: utf-8 -*-
"""
Created on Tue May  8 13:15:31 2012

@author: gofrendi
"""

from Go_GrammaticalEvolution import Go_GrammaticalEvolution
from scipy.stats.stats import pearsonr
from numpy import std

class Go_GEFCS(Go_GrammaticalEvolution):
    
    def _uniqueList(self, inlist): 
        # order preserving
        uniques = []
        for item in inlist:
            if item not in uniques:
                uniques.append(item)
        return uniques

    def _featureFitness(self, dimension, target):
        overlap_penalty = 0.5
        different_neighbor_penalty = 0.01
        cluster_count = len(self._uniqueList(target))
        ideal_different_neighbor_count = cluster_count -1
        
        dimension_target = []
        for i in xrange(len(dimension)):
            dimension_target.append([dimension[i], target[i]])
        dimension_target.sort()
        
        bad = 0.0    
        different_neighbor_count = 0 
        for i in xrange(len(dimension_target)):
            if(i>=0) and (i<len(dimension_target)-1):  
                if dimension_target[i+1][1] != dimension_target[i][1]:
                    different_neighbor_count += 1
                    if different_neighbor_count>ideal_different_neighbor_count:
                        bad += different_neighbor_penalty 
                    if dimension_target[i+1][0] == dimension_target[i][0]:
                        bad += overlap_penalty
        return (1/(0.001+bad))/1000
    
    def _fitnessFunction(self, chromosome): 
        #all variable here are written by using underscore prefix
        expr, level = self._evolve(chromosome)
        #if we've calculate this kind of phenotype before, just return the value, don't calculate it again
        if expr in self.calculatedPhenotype:
            return self.calculatedPhenotype[expr]
            
        result = 0 
        x=[]
        y=[] 
        fitness = 0      
        for trainingSetData in self.trainingSet['data']:
            predict, target, error = self._execExpr(expr, trainingSetData)
            if not error:
                x.append(predict)
                y.append(target)
            else:
                x=[]
                y=[]
                break
                        
        if (len(x)==0) or (len(y)==0) or (std(y)==0) or (std(x)==0):
            fitness = 0
        else:
            #result, p = pearsonr(x, y)
            result = self._featureFitness(x, y)
            fitness = result
            
        fitness -= 0.00000001 * level #the depth of the phenotype   
        self.calculatedPhenotype[expr] = fitness
        return fitness

    def getBestPhenotype(self, much=1, minimumFitness=0):
        #The best phenotypes with no correlation between each others
        featureDatas = []
        dictionary = self.calculatedPhenotype
        i=0
        featureCount = 0
        phenotype=[]
        for word in sorted(dictionary, key=dictionary.get,reverse=True):
            #stop if we're done
            if (featureCount>=much) or (float(dictionary[word])<minimumFitness):
                break
            #get current data (from phenotype to data)
            currentData=[]
            for trainingSetData in self.trainingSet['data']:
                predict, target, error = self._execExpr(word, trainingSetData)
                currentData.append(predict)
            #check correlation with already selected phenotype's data
            correlated = False
            for featureData in featureDatas:
                corr, p = pearsonr(currentData, featureData)
                if abs(corr)>0.5:
                    correlated = True
                    break
            #only add it whenever it's not correlated with already selected phenotype's data
            if not correlated:
                phenotype.append(word)
                featureDatas.append(currentData)
                featureCount += 1
            i+=1
        return phenotype
    
if __name__ == '__main__':
    gfcs = Go_GEFCS()
    gfcs.train()
    gfcs.printAllPhenotype()
    best = gfcs.getBestPhenotype(10,0.0)
    for individu in best:
        print(individu)