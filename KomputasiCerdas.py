# -*- coding: utf-8 -*-
"""
Created on Thu May 10 04:48:21 2012

@author: gofrendi
"""

#from Go_GrammaticalEvolution import Go_GrammaticalEvolution
from Go_GEFCS import Go_GEFCS
from Go_Random import Go_Random
from randomFunction import randomFunction
from thresholdingData import thresholdingData

ge = Go_GEFCS()
ge.random = Go_Random(randomFunction)
ge.grammar = {
    '<EXPR>' : [
            {'become' : '(<EXPR>)<OP>(<EXPR>)', 'p' : 3},
            {'become' : '<VAR>', 'p' : 5},
            {'become' : '<NUM>', 'p' : 2}
        ],
    '<OP>' : [
            {'become' : '+', 'p' : 4},
            {'become' : '-', 'p' : 3},
            {'become' : '*', 'p' : 3},
            {'become' : '/', 'p' : 3},
            {'become' : '**', 'p' : 1}
        ],
    '<VAR>' : [
            {'become' : 'otsu', 'p' : 5},
            {'become' : 'stdev', 'p' : 5},
            {'become' : 'mean', 'p' : 5},
            {'become' : 'minOtsu', 'p' : 5},
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
ge.startExpr = '<EXPR>'



trainingSet = {
        'header' : ['otsu', 'stdev', 'mean', 'minOtsu', 't'],
        'target' : 't',
        'data' : thresholdingData
    }
ge.trainingSet = trainingSet

ge.train()
ge.printAllPhenotype()

#good features should have correlation with the output (done),
#good features should not be correlated each other
bestPhenotype = ge.getBestPhenotype(5, 0)
for phenotype in bestPhenotype:
    print(phenotype)
    
all_inputs = []
all_targets = []
trainingHeader = trainingSet['header']
for trainingData in trainingSet['data']:
    sandbox = {}  
    inputs = []
    targets = []  
    for i in xrange(len(trainingHeader)):
        exec(trainingHeader[i]+'='+str(float(trainingData[i]))) in sandbox
    for i in xrange(len(bestPhenotype)):
        exec('_result = '+str(bestPhenotype[i])) in sandbox
        inputs.append(float(sandbox['_result']))
    exec('_result = '+str(trainingSet['target'])) in sandbox
    #targets.append(sandbox['_result'])
    targets = float(sandbox['_result'])
    all_inputs.append(inputs)
    all_targets.append(targets)

print all_inputs
print all_targets


from sklearn import svm
clf = svm.SVR(kernel='linear', scale_C=True)
clf.fit(all_inputs, all_targets)
print(clf.predict(all_inputs))