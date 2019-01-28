import scipy
import numpy
import scipy.fftpack
import scipy.io
import scipy.ndimage
import matplotlib.pyplot as plt
import PIL
import csv
#import pandas
from mpl_toolkits.mplot3d import Axes3D
#from skimage.feature.peak import peak_local_max
#from sklearn.cluster import KMeans



#dataset = ['7zip_6_11_18', 'aobench_6_11_18', 'cyclictest_6_11_18', 'flac_6_11_18', 'gimp_6_11_18', 'git_6_11_18', 'idle_6_11_18', 'opencv_6_11_18', 'phpbench_6_11_18', 'ramspeed_6_11_18', 'stream_6_11_18', 'tiny_6_11_18', 'ttest_6_11_18']
#dataset = ['ttest_6_11_18']
#dataset = ['initData']
dataset = ['SM0_FP_ADD']


def extractPowermap(dataset):
    # Open mask
    mask = PIL.Image.open('./data/' + dataset + '/' + dataset + ' - Box 1.bmp').convert('LA')
    mask = mask.convert('1')
    mask = numpy.asarray(mask)
    
    i = 0
    while True:
        i = i+1
        
        try:
            # Open raw heatmap
            reader = csv.reader(open('./data/' + dataset + '/' + dataset + '_' + str(i) + '.csv', "r"), delimiter=",")
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
            dct[9:, :] = 0
            dct[:, 9:] = 0
            # Inverse DCT to go back to original heatmap but without the noise
            idct = scipy.fftpack.idct(scipy.fftpack.idct(dct.T, norm='ortho').T, norm='ortho')
            lap = scipy.ndimage.filters.laplace(idct)
            
            # Sources are the max
            lap = -lap
            
            
#            # Plot filtered heatmap (idct)
#            fig = plt.figure()
#            ax = fig.gca(projection='3d')
#            surf = ax.plot_surface(X, Y, idct)
#            plt.show()
               
            
            # Sources are the max
            lap = -lap

            # Save the filtered powermap
            numpy.savetxt('./data/' + dataset + '/powermaps/' + dataset + '_' + str(i) + '.csv', lap, delimiter=",")
            
        except:
            return      


def main():
    # Extract powermap and transient power from thermalmaps
    i = 0
    while True:
        try:
            # Print status to monitor progress
            status = 'Extracting powermaps for dataset ' + dataset[i]
            print(status)
            
            if (i == 0):
                powerFullStack = extractPowermap(dataset[i])
            else:
                powerFullStack = numpy.vstack((powerFullStack, extractPowermap(dataset[i])))
            
            i = i+1
        
        except:            
            break

    return
        


if __name__== "__main__":
  main()