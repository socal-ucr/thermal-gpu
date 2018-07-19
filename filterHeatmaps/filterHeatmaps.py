import scipy
import numpy
import scipy.fftpack
import scipy.io
import scipy.ndimage
import matplotlib.pyplot as plt
import PIL
import csv
from mpl_toolkits.mplot3d import Axes3D
from skimage.feature.peak import peak_local_max


#dataset = '2cores10Frames'
dataset = 'initData'



def main():
    # Open mask
    #mask = PIL.Image.open('./data/2cores10Frames/mask.bmp').convert('LA')
    mask = PIL.Image.open('./data/' + dataset + '/' + dataset + ' - Box 1.bmp').convert('LA')
    mask = mask.convert('1')
    mask = numpy.asarray(mask)
    
    i = 0
    while True:
        i = i+1
        
        try:
            # Open raw heatmap
            reader = csv.reader(open('./data/' + dataset + '/' + dataset + '_' + str(i) + '.csv', "rb"), delimiter=",")
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
            # Delete high-freq region
            dct[dct.shape[0] // 18:, :] = 0
            dct[:, dct.shape[1] // 18:] = 0
            # Inverse DCT to go back to original heatmap but without the noise
            idct = scipy.fftpack.idct(scipy.fftpack.idct(dct.T, norm='ortho').T, norm='ortho')
            lap = scipy.ndimage.filters.laplace(idct)
            
            
            # Sources are the max
            lap = -lap
            # Find all local maxima
            maxima = peak_local_max(lap)

            if (i == 1):
                maximaGlobal = maxima
            else:
                maximaGlobal = numpy.vstack((maximaGlobal, maxima))
            
        except:
            print(maximaGlobal)
            plt.plot(maximaGlobal[:,1], maximaGlobal[:,0], 'o')
            plt.show()
            break
        
    # Plot
    Axes3D(plt.figure()).plot_surface(X, Y, heatmap)
    Axes3D(plt.figure()).plot_surface(X, Y, idct)
    Axes3D(plt.figure()).plot_surface(X, Y, lap)
    #plt.plot(maxima[:,1], maxima[:,0], lap[maxima[:,0],maxima[:,1]], 'o')
    #plt.show()
    #plt.plot(maximaGlobal[:,1], maximaGlobal[:,0], 'o')
    #plt.show()



if __name__== "__main__":
  main()