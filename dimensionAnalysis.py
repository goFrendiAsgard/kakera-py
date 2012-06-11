'''
Created on May 16, 2012

@author: gofrendi
'''

from numpy import mean, std
from numpy import random as rnd
from scipy.stats.stats import pearsonr

def uniqueList(inlist): 
    # order preserving
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques

def normalize(lst):
    maxVal = max(lst)
    minVal = min(lst)
    i = 0
    while i<len(lst):
        lst[i] = (lst[i]-minVal)/(maxVal-minVal)
        i +=1 
               
    return lst

def performNN(all_extracted_features, all_targets):
    from pyneurgen.neuralnet import NeuralNet
    #from pyneurgen.nodes import BiasNode, Connection
    net = NeuralNet()
    net.init_layers(len(all_extracted_features[0]), [2], 1)
    
    net.randomize_network()
    net.set_halt_on_extremes(True)
    
    #   Set to constrain beginning weights to -5 to 5
    #       Just to show we can
    #net.set_random_constraint(.5)
    net.set_learnrate(.001)
    
    net.set_all_inputs(all_extracted_features)
    net.set_all_targets(all_targets)
    
    length = len(all_extracted_features)
    learn_end_point = int(length * .8)
    
    net.set_learn_range(0, learn_end_point)
    net.set_test_range(learn_end_point + 1, length - 1)
    
    net.layers[1].set_activation_type('tanh')
    net.learn(epochs=150, show_epoch_results=True, random_testing=True)
    mse = net.test()
    print mse

def performSVM(input, target):
    from sklearn import svm
    clf = svm.SVC(kernel='linear',probability=True, C=1.0)
    clf.fit(input, target)
    print(clf.predict(input))
    return clf

def goodness(dimension, target):
    overlap_penalty = 0.1
    different_neighbor_penalty = 0.01
    cluster_count = len(uniqueList(target))
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
    #return bad

def overlapCount(dimension, target):
    clusters = uniqueList(target)    
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
        
    # the criterion: betweenClassVarriance
    return (1/(0.001+overlap))/1000



def betweenClassVariance(dimension, target):
    clusters = uniqueList(target)    
    clusteredDimension = {}
    meanDimension = mean(dimension)
    meanClusteredDimension = {}
    countClusteredDimension = {}
    countData = len(dimension)
    for cluster in clusters:
        clusteredDimension[cluster] = []
        countClusteredDimension[cluster] = 0
        for i in xrange(len(dimension)):
            if target[i]==cluster:
                clusteredDimension[cluster].append(dimension[i])
                countClusteredDimension[cluster] += 1
        meanClusteredDimension[cluster] = mean(clusteredDimension[cluster])
    # the criterion: betweenClassVarriance
    betweenClassVarriance = 0
    for cluster in clusters:
        betweenClassVarriance += float(countClusteredDimension[cluster])/countData * pow(meanClusteredDimension[cluster]-meanDimension, 2)
    return betweenClassVarriance

def corr(dimension, target):
    corr, p = pearsonr(dimension, target)
    return corr

def printAll(label, dimension, target):
    print('Variable : %s {%s}\t betweenClassVarriance  : %5.3f,\t correlation : %5.3f,\t nonOverlapped : %5.3f goodness : %5.3f ' % (label, ','.join(map(str,dimension)), betweenClassVariance(dimension,target), corr(dimension,target), overlapCount(dimension, target), goodness(dimension, target)))

x=[0, 0,-1,-2, 0,-3, 0,-4, 0,-5, 0,-6, 0, 0, 0, 1, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0,]
y=[0,-1, 0, 0,-2, 0,-3, 0,-4, 0,-5, 0,-6, 0, 1, 0, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6,]
t=[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,]


d1=[]
for i in xrange(len(x)):
    d1.append(x[i]**2+y[i]**2) 

d2=[0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1] 

d3=[]
for i in xrange(len(x)):
    d3.append(rnd.randint(1000))  

d4=[]
for i in xrange(len(x)):
    d4.append(rnd.randint(100)) 



if __name__ == '__main__':
    printAll('x', x, t)
    printAll('y', y, t)
    printAll('t', t, t)    
    printAll('d1', d1, t)
    printAll('d2', d2, t)
    printAll('d3', d3, t)
    printAll('d4', d4, t)
    
    #inputs = []
    #for inputElement in d1:
    #    inputs.append([inputElement])
    #    
    #targets = t
    #clf = performSVM(inputs, targets)
    
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    from skimage.io import imread
    mark=['wo','b^','ws']
    
    matplotlib.rcParams['axes.unicode_minus'] = False
    fig = plt.figure()
    ax = fig.add_subplot(111)    
    for i in xrange(len(x)):
        ax.plot(x[i], y[i], mark[t[i]])
    ax.set_title('Data')
    ax.set_ylim(ymin=-7, ymax=7)
    ax.set_xlim(xmin=-7, xmax=7)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    
    matplotlib.rcParams['axes.unicode_minus'] = False
    fig = plt.figure()
    ax = fig.add_subplot(111)    
    for i in xrange(len(d1)):
        ax.plot(d1[i], 0, mark[t[i]])
    ax.set_title('Data')
    ax.set_xlim(xmin=-1, xmax=40)
    plt.xlabel('x^2 + y^2')
    #plt.ylabel('y')
    plt.show()
    
    matplotlib.rcParams['axes.unicode_minus'] = False
    image_names = ['camera', 'text', 'jammed', 'recipe', 'article']
    for i in xrange(len(image_names)):
        #real image
        plt.subplot(2,5,i+1)
        image = imread("images/%s.png" %(image_names[i]))
        plt.imshow(image, cmap=plt.cm.gray)
        plt.title("%s" %(image_names[i]))
        #ground truth
        plt.subplot(2,5,5+i+1)
        image = imread("images/%s-groundtruth.png" %(image_names[i]))
        plt.imshow(image, cmap=plt.cm.gray)
        plt.title("%s groundtruth" %(image_names[i]))
    plt.show()  
    
    