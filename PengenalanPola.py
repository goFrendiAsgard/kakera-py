# -*- coding: utf-8 -*-
"""
Created on Thu May 10 04:48:21 2012

@author: gofrendi
"""

#from Go_GrammaticalEvolution import Go_GrammaticalEvolution
from Go_GEFCS import Go_GEFCS
from Go_Random import Go_Random
from randomFunction import randomFunction
from abaloneData import abaloneData

ge = Go_GEFCS()
ge.random = Go_Random(randomFunction)
ge.crossoverRate = 30
ge.mutationRate = 10
ge.newRate = 20
ge.elitismRate = 5
ge.maxEpoch = 60
ge.populationSize = 300
ge.maxCodon = 25
ge.startExpr = '<EXPR>'
ge.grammar = {
    '<EXPR>' : [
            {'become' : '(<EXPR>)<OP>(<EXPR>)', 'p' : 3},
            {'become' : '<VAR>', 'p' : 8},
            {'become' : '<NUM>', 'p' : 1}
        ],
    '<OP>' : [
            {'become' : '+', 'p' : 4},
            {'become' : '-', 'p' : 3},
            {'become' : '*', 'p' : 4},
            {'become' : '/', 'p' : 2},
            {'become' : '**', 'p' : 1}
        ],
    '<VAR>' : [
            {'become' : 'sex', 'p' : 3},
            {'become' : 'length', 'p' : 3},
            {'become' : 'diameter', 'p' : 3},
            {'become' : 'height', 'p' : 3},
            {'become' : 'whole_weight', 'p' : 3},
            {'become' : 'shucked_weight', 'p' : 3},
            {'become' : 'viscera_weight', 'p' : 3},
            {'become' : 'shell_weight', 'p' : 3},
            {'become' : 'rings', 'p' : 3},
        ],
    '<NUM>' : [
            {'become' : '<DIGIT>.<DIGIT>', 'p' : 1},
            {'become' : '<DIGIT>', 'p' : 9}
        ],
    '<DIGIT>' : [
            {'become' : '<DIGIT><DIGIT>', 'p' : 1},
            {'become' : '0', 'p' : 2},
            {'become' : '1', 'p' : 2},
            {'become' : '2', 'p' : 2},
            {'become' : '3', 'p' : 2},
            {'become' : '4', 'p' : 2},
            {'become' : '5', 'p' : 2},
            {'become' : '6', 'p' : 2},
            {'become' : '7', 'p' : 2},
            {'become' : '8', 'p' : 2},
            {'become' : '9', 'p' : 2}
        ]
}



trainingSet = {
        'header' : ['sex', 'length', 'diameter', 'height', 'whole_weight', 'shucked_weight', 'viscera_weight', 'shell_weight', 'rings'],
        'target' : 'rings',#'rings+1.5',
        'data' : abaloneData
    }
ge.trainingSet = trainingSet
    
ge.train()
ge.printAllPhenotype()

#good features should have correlation with the output (done),
#good features should not be correlated each other
bestPhenotype = ge.getBestPhenotype(4, 0)
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
all_predicts = clf.predict(all_inputs)
print(all_predicts)

right = 0
wrong = 0
mse = 0.0
for i in xrange(len(all_targets)):
    mse += pow((all_targets[i]-all_predicts[i]), 2)
    if abs(all_targets[i]-all_predicts[i])>1:
        wrong +=1
    else:
        right +=1
mse = pow(mse, 0.5)
print('right : %d, wrong : %d, mse : %5.3f' %(right, wrong, mse))