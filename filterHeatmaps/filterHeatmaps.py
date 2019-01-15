#!/usr/bin/env python

import scipy
import numpy
import scipy.fftpack
import scipy.io
import scipy.ndimage
import matplotlib.pyplot as plt
import PIL
import csv
import argparse
from mpl_toolkits.mplot3d import Axes3D
from skimage.feature.peak import peak_local_max
from os import listdir
from os.path import isfile, join


def getSteadyMask(args):
    datasetPath = ('./data/' + args.dataset + '/')
    #determine last frame to capture steady state
    onlyfiles = [f for f in listdir(datasetPath) if isfile(join(datasetPath, f))]
    lastFrame = len(onlyfiles) - 3

    # Open mask
    mask = PIL.Image.open(datasetPath + args.dataset + ' - Box 1.bmp').convert('LA')
    mask = mask.convert('1')
    mask = numpy.asarray(mask)
    

    # Open raw heatmap
    reader = csv.reader(open(datasetPath + args.dataset + '_' + str(lastFrame) + '.csv', "rb"), delimiter=",")
    x = list(reader)
    heatmap = numpy.array(x).astype("float")
    # Apply mask
    heatmap = numpy.ma.masked_array(heatmap, ~mask)
    # Crop masked region (Region of interest: ROI)
    si, se = numpy.where(~heatmap.mask)
    heatmap = heatmap[si.min():si.max() + 1, se.min():se.max() + 1]
    
    X, Y = numpy.meshgrid(range(heatmap.shape[1]), range(heatmap.shape[0]))
    # Discrete Cosine Transform (DCT) of heatmap
    dct = scipy.fftpack.dct(scipy.fftpack.dct(heatmap.T, norm='ortho').T, norm='ortho')
    # Delete high-freq region
    dct[dct.shape[0] // args.filter:, :] = 0
    dct[:, dct.shape[1] // args.filter:] = 0
    # Inverse DCT to go back to original heatmap but without the noise
    idct = scipy.fftpack.idct(scipy.fftpack.idct(dct.T, norm='ortho').T, norm='ortho')
    

    #normailze
    idct = (idct - idct.min()) / (idct.max() - idct.min())
    idct = idct - float(0.5)

    return idct

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--filter', type=int, dest='filter', default=18, help='how much to filter high freqiences')
    parser.add_argument('--dataset', type=str, dest='dataset', default='2cores10Frames', help='path of dataset')
    args = parser.parse_args()

    steadyMask = getSteadyMask(args);

    # Open mask
    mask = PIL.Image.open('./data/' + args.dataset + '/' + args.dataset + ' - Box 1.bmp').convert('LA')
    mask = mask.convert('1')
    mask = numpy.asarray(mask)
    
    i = 0
    
    while True:
        i = i+1
        
        try:
            # Open raw heatmap
            reader = csv.reader(open('./data/' + args.dataset + '/' + args.dataset + '_' + str(i) + '.csv', "rb"), delimiter=",")
            x = list(reader)
            heatmap = numpy.array(x).astype("float")
            # Apply mask
            heatmap = numpy.ma.masked_array(heatmap, ~mask)
            # Crop masked region (Region of interest: ROI)
            si, se = numpy.where(~heatmap.mask)
            heatmap = heatmap[si.min():si.max() + 1, se.min():se.max() + 1]
            
            # Get shape of ROI
            X, Y = numpy.meshgrid(range(heatmap.shape[1]), range(heatmap.shape[0]))
            
            # Discrete Cosine Transform (DCT) of heatmap
            dct = scipy.fftpack.dct(scipy.fftpack.dct(heatmap.T, norm='ortho').T, norm='ortho')
            # Delete high-freq region in diagonal pattern, this is determined by the --filter option
            # --filter 10 means only allow top 10 frequencies 
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
                    
                    if ind > args.filter:
                        dct[i,j] = 0
                    ind += 1

                while (j - 1 >= 0 and i + 1 < n):
                    i += 1
                    j -= 1
                    if ind > args.filter:
                        dct[i,j] = 0
                    ind += 1

                if (j + 1 < m or i + 1 < n):
                    if (i + 1 < n):
                        i += 1
                    elif (j + 1 < m):
                        j += 1
                    if ind > args.filter:
                        dct[i,j] = 0
                    ind += 1

                while (j + 1 < m and i - 1 >= 0):
                    i -= 1
                    j += 1
                    if ind > args.filter:
                        dct[i,j] = 0
                    ind += 1
            #dct[dct.shape[0] // args.filter:, :] = 0
            #dct[:, dct.shape[1] // args.filter:] = 0
            # Inverse DCT to go back to original heatmap but without the noise
            idct = scipy.fftpack.idct(scipy.fftpack.idct(dct.T, norm='ortho').T, norm='ortho')

            #subtract steady state filter
            #idct = idct - ((idct.max()*0.4) * steadyMask)

            lap = scipy.ndimage.filters.laplace(idct)
            
            # Sources are the max
            lap = -lap
            # Find all local maxima
            maxima = peak_local_max(lap)
            
            if (i == 1):
                maximaGlobal = maxima
            else:
                maximaGlobal = numpy.vstack((maximaGlobal, maxima))

            #Filtered Heatmap
            #Axes3D(plt.figure()).plot_surface(X, Y, heatmap)

            #heat sources
            # plt.plot(maximaGlobal[:,1], maximaGlobal[:,0], 'o')

            plt.savefig(str(i)+'.jpg')
           # plt.clf()
        except:
            #print(maximaGlobal)
            #plt.plot(maximaGlobal[:,1], maximaGlobal[:,0], 'o')
           # plt.savefig(str(args.filter)+'.jpg')
           # plt.show()
            break
        
    # Plot
    #Axes3D(plt.figure()).plot_surface(X, Y, heatmap)
    #Axes3D(plt.figure()).plot_surface(X, Y, idct)
    #Axes3D(plt.figure()).plot_surface(X, Y, lap)
    #plt.plot(maxima[:,1], maxima[:,0], lap[maxima[:,0],maxima[:,1]], 'o')
    #plt.show()
    #plt.plot(maximaGlobal[:,1], maximaGlobal[:,0], 'o')
    #plt.show()



if __name__== "__main__":
    main()
