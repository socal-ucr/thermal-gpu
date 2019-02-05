#!/usr/bin/env python
import scipy
import numpy as np
import numpy.matlib
import scipy.fftpack
import scipy.io
import scipy.ndimage
import matplotlib.pyplot as plt
import PIL
import csv
import argparse
import pandas
from mpl_toolkits.mplot3d import Axes3D
from skimage.feature.peak import peak_local_max
from sklearn import mixture
from matplotlib.colors import LogNorm
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


readDir = '/mnt/SharedData/'
writeDir = './data/'
dataset = ['FP_ADD']
#dataset = ['FP_ADD', 'INT_ADD', 'SFU_SIN', 'L1_CACHE']
#dataset = ['L2_CACHE']
#dataset = ['0_FP_ADD', '0_INT_ADD', '0_L1_CACHE', '0_L2_CACHE', '0_SFU_SIN',
#           '1_FP_ADD', '1_INT_ADD', '1_L1_CACHE', '1_L2_CACHE', '1_SFU_SIN',
#           '2_FP_ADD', '2_INT_ADD', '2_L1_CACHE', '2_L2_CACHE', '2_SFU_SIN']


#Global Variables
maximaSM = np.empty([1,2])
SM0Polygon = Polygon([[45,105],[75,105],[75,125],[45,125]])

def findKnee(maxima, lap):
    maximaAmplitude = []

    for element in maxima:
        maximaAmplitude.append(lap[element[0],element[1]])

    sortedMaxima = [x for _,x in sorted(zip(maximaAmplitude,maxima), reverse=True)]
    maximaAmplitude.sort(reverse=True)
    maximaAmplitude = maximaAmplitude[:len(maximaAmplitude)//2]

    nPoints = len(maximaAmplitude)
    allCoord = np.vstack((range(nPoints),maximaAmplitude)).T
    
    firstPoint = allCoord[0]
    # get vector between first and last point - this is the line
    lineVec = allCoord[-1] - allCoord[0]
    lineVecNorm = lineVec / np.sqrt(np.sum(lineVec**2))

    # find the distance from each point to the line:
    # vector between all points and first point
    vecFromFirst = allCoord - firstPoint

    scalarProduct = np.sum(vecFromFirst * np.matlib.repmat(lineVecNorm, nPoints, 1), axis=1)
    vecFromFirstParallel = np.outer(scalarProduct, lineVecNorm)
    vecToLine = vecFromFirst - vecFromFirstParallel

    # distance to line is the norm of vecToLine
    distToLine = np.sqrt(np.sum(vecToLine ** 2, axis=1))

    # knee/elbow is the point with max distance value
    idxOfBestPoint = np.argmax(distToLine)
    
    return np.array(sortedMaxima[:idxOfBestPoint+1]) 

def filterDCT(dct,numFeatures):
    # Delete high-freq region
    i = 0
    j = 0
    n = dct.shape[0]
    m = dct.shape[1]
    ind = 2
    while ind < dct.shape[0]*dct.shape[1]:
        if (j + 1 < m or i + 1 < n):
            if (j+1 < m):
                j += 1
            elif (i + 1 < n):
                i +=1
            
            if ind > numFeatures:
                dct[i,j] = 0
            ind += 1

        while (j - 1 >= 0 and i + 1 < n):
            i += 1
            j -= 1
            if ind > numFeatures:
                dct[i,j] = 0
            ind += 1

        if (j + 1 < m or i + 1 < n):
            if (i + 1 < n):
                i += 1
            elif (j + 1 < m):
                j += 1

            if ind > numFeatures:
                dct[i,j] = 0

            ind += 1

        while (j + 1 < m and i - 1 >= 0):
            i -= 1
            j += 1
            if ind > numFeatures:
                dct[i,j] = 0
            ind += 1
    return dct

def extractPowermap(dataset, args):
    # Open mask
    mask = PIL.Image.open( readDir + dataset + '/' + dataset + ' - Box 1.bmp').convert('LA')
    mask = mask.convert('1')
    mask = np.asarray(mask)
    i = 500
    while True:
        i = i+1
        
        try:
            # Open raw heatmap
            reader = csv.reader(open( readDir + dataset + '/' + dataset + '_' + str(i) + '.csv', "r"), delimiter=",")
            x = list(reader)
            heatmap = np.array(x).astype("float")
            # Apply mask
            heatmap = np.ma.masked_array(heatmap, ~mask)
            # Crop masked region (Region of interest: ROI)
            si, se = np.where(~heatmap.mask)
            heatmap = heatmap[si.min():si.max() + 1, se.min():se.max() + 1]
            
            # Get shape of ROI
            X, Y = np.meshgrid(range(heatmap.shape[1]), range(heatmap.shape[0]))
            
            # Discrete Cosine Transform (DCT) of heatmap
            dct = scipy.fftpack.dct(scipy.fftpack.dct(heatmap.T, norm='ortho').T, norm='ortho')

            #Filter DCT
            dct = filterDCT(dct, args.filter)

            # Inverse DCT to go back to original heatmap but without the noise
            idct = scipy.fftpack.idct(scipy.fftpack.idct(dct.T, norm='ortho').T, norm='ortho')
            lap = scipy.ndimage.filters.laplace(idct)
            
            # Sources are the max
            lap = -lap
            
            # Find all local maxima
            maxima = peak_local_max(lap)
            #Get only the highest amplitudes
            maxima = findKnee(maxima,lap)

            global maximaSM
            maximaSM = np.vstack((maximaSM, maxima))

            # Plot filtered heatmap (idct)
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            surf = ax.plot_surface(X, Y, lap)
            plt.plot(maxima[:,1], maxima[:,0], lap[maxima[:,0],maxima[:,1]], 'o')
            plt.show()
            exit()
            #plt.savefig(str(args.filter)+'power.jpg')
            # Save the filtered powermap
            #np.savetxt( writeDir + dataset + '/powermaps/' + dataset + '_' + str(i) + '.csv', lap, delimiter=",")
        except Exception as e:
            if i == 1:
                print(e)
            return


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--filter', type=int, dest='filter', default=81, help='how much to filter high freqiences')
    args = parser.parse_args()

    # Extract powermap and transient power from thermalmap
    
    for SM in range(1):
        for uBM in dataset:
            # Print status to monitor progress
            status = 'Extracting powermaps for dataset ' + str(SM) + '_' + uBM
            print(status)
            extractPowermap(str(SM) + '_' + uBM,args)
            
            

            global maximaSM
            SM0Points = []
            for element in maximaSM:
                if SM0Polygon.contains(Point(element[1],element[0])):
                    SM0Points += [element]
        
            SM0Points = np.array(SM0Points)
            plt.plot(SM0Points[:,1], SM0Points[:,0], 'o')
            #np.savetxt(str(SM)+"_L2Cache.csv",maximaSM,delimiter=',')
            maximaSM = np.empty([1,2])


    plt.savefig('SM0.pdf',bbox_inshes="tight")
    plt.show()
    return
        

if __name__== "__main__":
  main()
