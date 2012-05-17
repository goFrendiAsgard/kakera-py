# -*- coding: utf-8 -*-
"""
Created on Tue May  8 13:15:31 2012

@author: gofrendi
"""

from Go_GrammaticalEvolution import Go_GrammaticalEvolution
from scipy.stats.stats import pearsonr
from numpy import std

from numpy import mean

class Go_GEFCS(Go_GrammaticalEvolution):
    
    def _uniqueList(self, inlist): 
        # order preserving
        uniques = []
        for item in inlist:
            if item not in uniques:
                uniques.append(item)
        return uniques

    def _featureFitness(self, dimension, target):
        clusters = self._uniqueList(target)    
        clusteredDimension = {}
        minVal = {}
        maxVal = {}
        #means = {}
        #stdev = {}
        for cluster in clusters:
            clusteredDimension[cluster] = []
            for i in xrange(len(dimension)):
                if target[i]==cluster:
                    clusteredDimension[cluster].append(dimension[i])
            minVal[cluster] = min(clusteredDimension[cluster])
            maxVal[cluster] = max(clusteredDimension[cluster])
            #means[cluster] = mean(clusteredDimension[cluster])
            #stdev[cluster] = std(clusteredDimension[cluster])
        
        overlap = 0
        for i in xrange(len(clusters)):
            iCluster = clusters[i]
            for j in xrange(i+1,len(clusters)):
                jCluster = clusters[j]
                if minVal[iCluster]<=maxVal[jCluster] and minVal[iCluster]>=minVal[jCluster]:
                    limit = min([maxVal[iCluster], maxVal[jCluster]])
                    overlap += float(limit)-float(minVal[iCluster])+1
                elif maxVal[iCluster]<=maxVal[jCluster] and maxVal[iCluster]>=minVal[jCluster]:
                    limit = max([minVal[iCluster], minVal[jCluster]])
                    overlap += float(maxVal[iCluster])-float(limit)+1
        # the criterion: minimum overlap
        return (1/(0.001+overlap))/1000
    
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