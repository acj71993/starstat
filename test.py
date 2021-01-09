# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 12:45:08 2020

@author: acj71
"""
from photutils.datasets import make_100gaussians_image
from photutils import CircularAperture, CircularAnnulus
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import rawpy
import imageio
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
import startools as st


files = ['DSC00325.ARW','DSC00326.ARW']
img = st.get_images(files)


