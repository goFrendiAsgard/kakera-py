# -*- coding: utf-8 -*-
"""
Created on Sat May 12 09:47:38 2012

@author: gofrendi
"""

import matplotlib.pyplot as plt

from skimage.io import imread
from skimage.io import imsave
from skimage.filter import threshold_otsu
from scipy import std, mean

def getImageFeature(imagefile, m=3, n=3):
    image = imread(imagefile)
    imagePartHeight = len(image) / m
    imagePartWidth = len(image[0]) / n
    data = []
    imagePart = []
    for i in xrange(m):
        imagePart.append([])
        for j in xrange(n):
            imagePart[i].append([])
            imagePart[i][j] = image[i*imagePartHeight:(1+i)*imagePartHeight, j*imagePartWidth:(1+j)*imagePartWidth]
            newFilename = imagefile[0:-4]+'_'+str(i)+'_'+str(j)+'.png'
            imsave(newFilename, imagePart[i][j])
            thresh = threshold_otsu(imagePart[i][j])
            means = mean(imagePart[i][j])
            stdev = std(imagePart[i][j])
            record = [thresh, stdev, means]
            data.append(record)
            plt.subplot(m, n, i * m + j + 1)
            plt.title('otsu:%d,\nstdev:%3.2f,\nmeans:%3.2f' % (thresh, stdev, means))
            plt.imshow(imagePart[i][j], cmap=plt.cm.gray)
    
    for i in xrange(m):
        for j in xrange(n):
            neighborOtsu = []
            #3 tetangga atas
            if i>0:
                neighborOtsu.append(data[(i-1)*3+j][0])
                if j>0: #kiri atas
                    neighborOtsu.append(data[(i-1)*3+(j-1)][0])
                if j<n-1: #kanan atas
                    neighborOtsu.append(data[(i-1)*3+(j+1)][0])
            #3 tetangga bawah
            if i<m-1:
                neighborOtsu.append(data[(i+1)*3+j][0])
                if j>0: #kiri bawah
                    neighborOtsu.append(data[(i+1)*3+(j-1)][0])
                if j<n-1: #kanan bawah
                    neighborOtsu.append(data[(i+1)*3+(j+1)][0])
            #kiri
            if j>0:
                neighborOtsu.append(data[i*3+(j-1)][0])
            #kanan
            if j<n-1:
                neighborOtsu.append(data[i*3+(j+1)][0])
            minOtsu = min(neighborOtsu)
            data[(i*3)+j].append(minOtsu)
            
    print data
    plt.show()        
    return data

getImageFeature('/home/gofrendi/Documents/kakera-py/images/camera.png')
getImageFeature('/home/gofrendi/Documents/kakera-py/images/text.png')
getImageFeature('/home/gofrendi/Documents/kakera-py/images/jammed.png')
getImageFeature('/home/gofrendi/Documents/kakera-py/images/recipe.png')
getImageFeature('/home/gofrendi/Documents/kakera-py/images/article.png')