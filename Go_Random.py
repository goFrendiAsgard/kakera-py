# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 11:23:30 2012

@author: gofrendi
"""
import numpy.random as rnd

class Go_Random:
    
    def __init__(self, fn=None):
        # parameter:
        # * fn : a function that return 1 dimensional list of random number
        #   if there is no fn given, rnd.random(100) will be used
        self.index = 0
        self.list = []
        if fn==None:
            self.list = rnd.random(1000)
        else:
            self.list = fn()
            
    def __del__(self):
        del self.index
        del self.list
    
    def get(self, minVal=None, maxVal=None):
        #this function will get a member of the random number list and return it as float
        # parameter:
        # * minVal : minimum return value
        # * maxVal : maximum return value
        self.index += 1
        if(self.index >= len(self.list)):
            self.index = 0;
        number = float(self.list[self.index-1])
        if minVal!=None:
            minList = min(self.list)
            if maxVal !=None:
                maxList = max(self.list)
                number = minVal + number*(maxVal-minVal)/(maxList-minList)
            else:
                number = minVal + number - minList
        return number
    
    number = property(get, None, None, 'a random number')

if __name__ == '__main__':
    grand = Go_Random(lambda : rnd.random(100))
    for i in xrange(10):
        print(grand.number)
    
