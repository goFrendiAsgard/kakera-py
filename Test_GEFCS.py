# -*- coding: utf-8 -*-
"""
Created on Tue May  8 13:35:47 2012

@author: gofrendi
"""

from Go_GEFCS import Go_GEFCS
from Go_Random import Go_Random
from randomFunction import randomFunction
from thresholdingData import thresholdingData


gfcs = Go_GEFCS()
gfcs.random = Go_Random(randomFunction)
gfcs._grammar = {
    '<EXPR>' : [
            {'become' : '(<EXPR>)<OP>(<EXPR>)', 'p' : 2},
            {'become' : '<VAR>', 'p' : 8},
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

gfcs._trainingSet = {
        'header' : ['otsu', 'stdev', 'mean', 'minOtsu', 't'],
        'target' : 't',
        'data' : thresholdingData
    }

gfcs.train()
gfcs.printAllPhenotype()
best = gfcs.getBestPhenotype(10,0.0)
trainingSet = {}
trainingSet['target'] = gfcs._trainingSet['target']
trainingSet['header'] = []
trainingSet['data'] = []
for individu in best:
    print(individu)