from photutils.datasets import make_100gaussians_image
from photutils import CircularAperture, CircularAnnulus
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import rawpy
import imageio
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters

def loadraw(file):
    #load raw image file to rgb
    raw = rawpy.imread(file)
    rgb = raw.postprocess()
    return rgb

def get_percentile(x,beta):
    F = np.arange(0,len(x))/len(x)
    xs = np.sort(x)
    idx = F<=beta
    x0 = xs[idx]
    x0 = x0[len(x0)-1]
    return x0
    

def findpeaks(data,npeaks):
    #finds local maxima in 2D array
    xxx = data.reshape((np.size(data,0)*np.size(data,1)))
    threshold = get_percentile(xxx,.999)
    print('Star Brightness Threshold:')
    print(threshold)
    neighborhood_size = 300 #selection of this parameter should be automater (needs work)
    data_max = filters.maximum_filter(data, neighborhood_size)
    maxima = (data == data_max)
    data_min = filters.minimum_filter(data, neighborhood_size)
    diff = ((data_max - data_min) > threshold)
    maxima[diff == 0] = 0
    labeled, num_objects = ndimage.label(maxima)
    slices = ndimage.find_objects(labeled)
    x, y = [], []
    val = []
    for dy,dx in slices:
        x_center = (dx.start + dx.stop - 1)/2
        x.append(x_center)
        y_center = (dy.start + dy.stop - 1)/2    
        y.append(y_center)
        val.append(data[int(np.floor(y_center)),np.int(np.floor(x_center))])
    if len(x)<npeaks:
        npeaks = len(xp)
    #isolate top N stars based on brightness
    x = np.array(x)
    y = np.array(y)
    xsort = x[np.argsort(val)]
    ysort = y[np.argsort(val)]
    x = xsort[len(x)-1-npeaks:]
    y = ysort[len(y)-1-npeaks:]
    return x,y

def pre_process(rgb):
    data = rgb[:,:,1] #use only green channel (center of visible spectrum)
    data = ndimage.gaussian_filter(data,sigma = 1.0)
    return data

def get_images(files):
    #gathers list of images into array
    img = []
    n = -1
    for f in files:
        n = n+1
        img.append(star_image())
        img[n].raw = loadraw(f)
        img[n].data = pre_process(img[n].raw)
        #find top 20 stars
        img[n].xp,img[n].yp = findpeaks(img[n].data,50)
        #plot stars with estimated radius
        plt.figure()
        plt.gray()
        plt.imshow((img[n].data))
        plt.scatter(img[n].xp,img[n].yp,s = 80,facecolors = 'none',edgecolors = 'r')
    return img
    
def common_stars(img):
    #reduces set of star images to only common stars
    pass

def translate(img0,img):
    #translates img to be aligned with img0 based on common star patterns
    pass

class star_image():
    pass