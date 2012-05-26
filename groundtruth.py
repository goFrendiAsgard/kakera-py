# -*- coding: utf-8 -*-
"""
Created on Sat May 12 09:47:38 2012

@author: gofrendi
"""

import matplotlib.pyplot as plt
import os

from skimage.io import imread
#from skimage.io import imsave
from skimage.filter import threshold_otsu
from scipy import std, mean

def getImageFeature(imagefile, groundTruthImageFile, m=3, n=3):
    image = imread(imagefile)
    groundTruthImage = imread(groundTruthImageFile)
    imagePartHeight = len(image) / m
    imagePartWidth = len(image[0]) / n
    data = []
    imagePart = []
    groundTruthImagePart = []
    for i in xrange(m):
        imagePart.append([])
        groundTruthImagePart.append([])
        for j in xrange(n):
            imagePart[i].append([])
            groundTruthImagePart[i].append([])
            imagePart[i][j] = image[i*imagePartHeight:(1+i)*imagePartHeight, j*imagePartWidth:(1+j)*imagePartWidth]
            groundTruthImagePart[i][j] = groundTruthImage[i*imagePartHeight:(1+i)*imagePartHeight, j*imagePartWidth:(1+j)*imagePartWidth]
            #newFilename = imagefile[0:-4]+'_'+str(i)+'_'+str(j)+'.png'
            #imsave(newFilename, imagePart[i][j])
            
            
            
            bestTruePixel = 0
            bestThresh = 0
            for k in xrange(255):
                truePixel = 0
                for x in xrange(imagePartHeight):
                    for y in xrange(imagePartWidth):
                        if (groundTruthImagePart[i][j][x][y] == 0 and imagePart[i][j][x][y]<k) or (groundTruthImagePart[i][j][x][y] == 255 and imagePart[i][j][x][y]>k):
                            truePixel +=1
                if truePixel > bestTruePixel:
                    bestTruePixel = truePixel
                    bestThresh = k
                    print("%s (%d, %d), find bestThresh : %d" %(imagefile, i, j, bestThresh))
            
            thresh = threshold_otsu(imagePart[i][j])
            means = mean(imagePart[i][j])
            stdev = std(imagePart[i][j])
            record = [thresh, stdev, means, bestThresh]
            data.append(record)
            
            #plt.subplot(m, n, i * m + j + 1)
            #plt.title('otsu:%d,\nstdev:%3.2f,\nmeans:%3.2f' % (thresh, stdev, means))
            #plt.imshow(imagePart[i][j], cmap=plt.cm.gray)
    
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
            
    print(data)
    plt.show()        
    return data

if __name__ == '__main__':
    dir_path = os.path.dirname(__file__) 
    data = []   
    data.append(getImageFeature(os.path.join(dir_path, 'images/camera.png'), os.path.join(dir_path, 'images/camera-groundtruth.png')))
    data.append(getImageFeature(os.path.join(dir_path, 'images/text.png'), os.path.join(dir_path, 'images/text-groundtruth.png')))
    data.append(getImageFeature(os.path.join(dir_path, 'images/jammed.png'), os.path.join(dir_path, 'images/jammed-groundtruth.png')))
    data.append(getImageFeature(os.path.join(dir_path, 'images/recipe.png'), os.path.join(dir_path, 'images/recipe-groundtruth.png')))
    data.append(getImageFeature(os.path.join(dir_path, 'images/article.png'), os.path.join(dir_path, 'images/article-groundtruth.png')))
    print(data)
