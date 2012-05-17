# -*- coding: utf-8 -*-
"""
Created on Fri May  4 06:57:13 2012

@author: gofrendi
"""
from Go_GeneticsAlgorithm import Go_GeneticsAlgorithm

class Go_GrammaticalEvolution(Go_GeneticsAlgorithm):
    
    
    def __init__(self):
        Go_GeneticsAlgorithm.__init__(self)
        self.calculatedPhenotype = {}
        self.minCodon = 0
        self.maxCodon = 100
        self._startExpr = '<EXPR>'
        self._grammar = {
            '<EXPR>' : [
                    {'become' : '(<EXPR>)<OP>(<EXPR>)', 'p' : 3},
                    {'become' : '<VAR>', 'p' : 6},
                    {'become' : '<NUM>', 'p' : 1}
                ],
            '<OP>' : [
                    {'become' : '+', 'p' : 4},
                    {'become' : '-', 'p' : 3},
                    {'become' : '*', 'p' : 2},
                    {'become' : '/', 'p' : 1},
                    {'become' : '^', 'p' : 1}
                ],
            '<VAR>' : [
                    {'become' : 'x1', 'p' : 5},
                    {'become' : 'x2', 'p' : 5}
                ],
            '<NUM>' : [
                    {'become' : '<DIGIT>.<DIGIT>', 'p' : 2},
                    {'become' : '<DIGIT>', 'p' : 8}
                ],
            '<DIGIT>' : [
                    {'become' : '<DIGIT><DIGIT>', 'p' : 1},
                    {'become' : '0', 'p' : 1},
                    {'become' : '1', 'p' : 1},
                    {'become' : '2', 'p' : 1},
                    {'become' : '3', 'p' : 1},
                    {'become' : '4', 'p' : 1},
                    {'become' : '5', 'p' : 1},
                    {'become' : '6', 'p' : 1},
                    {'become' : '7', 'p' : 1},
                    {'become' : '8', 'p' : 1},
                    {'become' : '9', 'p' : 1}
                ]
        }
        self._trainingSet = {
            'header' : ['x1', 'x2', 'output'],
            'target' : 'output',
            'data' : [
                    [1, 1, 2],
                    [1, 2, 3],
                    [2, 1, 3],
                    [2, 2, 4],
                    [3, 1, 4],
                    [3, 2, 5],
                    [4, 3, 7],
                    [4, 4, 8]             
                ]
        }
    
    def _getStartExpr(self):
        return self._startExpr
    def _setStartExpr(self, startExpr):
        self._startExpr = startExpr
        if not (self._startExpr in self._grammar):
            self._startExpr = self._grammar.keys()[0]
    def _getGrammar(self):
        return self._grammar
    def _setGrammar(self, grammar):
        self._grammar = grammar
        if not (self._startExpr in self._grammar):
            self._startExpr = self._grammar.keys()[0]
    def _getTrainingSet(self):
        return self._trainingSet
    def _setTrainingSet(self, trainingSet):
        self._trainingSet = trainingSet
    
    def _evolve(self, chromosome):
        codonIndex = 0    
        depth = 10        
        expr = self.startExpr
        for level in xrange(depth):
            newExpr = ''
            i=0
            while i<len(expr):
                find = False
                for key in self.grammar:
                    if (expr[i:i+len(key)] == key):
                        find = True
                        #choose the rule
                        cump = 0
                        ruleIndex = 0
                        for j in xrange(len(self.grammar[key])):
                            if not ('p' in self.grammar[key][j]):
                                self.grammar[key][j]['p'] = 1
                            cump += self.grammar[key][j]['p']
                            self.grammar[key][j]['cum'] = cump
                        #calculate p
                        #print codonIndex
                        p = chromosome[codonIndex] % cump
                        #from p determine ruleIndex
                        for j in xrange(len(self.grammar[key])):
                            if p<=self.grammar[key][j]['cum']:
                                ruleIndex=j
                                break
                        #increase codon index
                        if codonIndex<len(chromosome)-1:
                            codonIndex += 1
                        else:
                            codonIndex = 0
                        #apply the rule
                        newExpr += self.grammar[key][ruleIndex]['become']
                        i+= len(key)-1
                if not find:
                    newExpr += expr[i:i+1]
                i+=1
            #if no change than break
            #else expr = newExpr
            if expr == newExpr:
                break
            else:
                expr = newExpr
            #print expr
        return expr, level
    
    def _execExpr(self, expr, record):
        predict = 0
        target = 0
        error = False
        
        try:
            sandbox={}
            for i in xrange(len(record)):       
                exec(self.trainingSet['header'][i]+' = '+str(record[i])) in sandbox             
            exec('__predict = '+expr) in sandbox
            exec('__target = '+self.trainingSet['target']) in sandbox 
                      
            predict = sandbox['__predict']
            target = sandbox['__target']
        except:
            error = True    
        return predict, target, error
        pass
    
    def _fitnessFunction(self, chromosome):
        #all variable here are written by using underscore prefix
        expr, level = self._evolve(chromosome)
        #if we've calculate this kind of phenotype before, just return the value, don't calculate it again
        if expr in self.calculatedPhenotype:
            return self.calculatedPhenotype[expr]
            
        result = 0        
        for trainingSetData in self.trainingSet['data']:
            predict, target, error = self._execExpr(expr, trainingSetData)
            if error:
                result += 10000 # if error, I assume the delta as 10000
            else:
                result += abs(predict-target) #the delta between predict & target
        
        result /= float(len(self.trainingSet['data'])) #this is the means absolute error
        result += 0.00000001 * level #the depth of the phenotype   
        fitness = (1/(float(result)+0.001))/1000
        self.calculatedPhenotype[expr] = fitness
        return fitness
        
    def getBestPhenotype(self, much=1, minimumFitness=0):
        dictionary = self.calculatedPhenotype
        i=0
        phenotype=[]
        for word in sorted(dictionary, key=dictionary.get,reverse=True):
            if (i>=much) or (float(dictionary[word])<minimumFitness):
                break
            phenotype.append(word)
            i+=1
        return phenotype
        
    def printAllPhenotype(self):
        dictionary = self.calculatedPhenotype
        for word in sorted(dictionary, key=dictionary.get, reverse=True):
            print ('Expression: %s' % (word))
            print ('Fitness: %3.10f' % float(dictionary[word]))
            print ('')
    
    grammar = property(_getGrammar, _setGrammar, None)
    trainingSet = property(_getTrainingSet, _setTrainingSet, None)
    startExpr = property(_getStartExpr, _setStartExpr, None)

if __name__ == '__main__':
    ge = Go_GrammaticalEvolution()
    ge.maxEpoch = 50
    ge.populationSize = 20
    ge.train()
    #print ge
    ge.printAllPhenotype()