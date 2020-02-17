# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 17:32:57 2018

@author: hollie_min
"""

# This is a module that includes basic image processing functions
import numpy as np
import skimage as sk
from skimage.filters import threshold_otsu
#from skimage import data, exposure, img_as_float

class Basic_processing:
    def __init__(self):
        pass
#        self.image = image
    
    
    mode = None    
    clip_limit = 0.01
    nbins = 256  
    thresh = None
    
#    function 1: histogram equalization, include both naive histogram strech and CLAHE adaptive histogram equalization
    def histogram_equalization(self):        
        
        if self.mode is 'hist_equal':
            
            im = sk.exposure.equalize_hist(self.image)
            
        if self.mode is 'CLAHE':# Contrast Limited Adaptive Histogram Equalization 
            self.thresh = None
            im = sk.exposure.equalize_adapthist(self.image,clip_limit = self.clip_limit, nbins = self.nbins)
            
        return im
#    function 2: thresholding, include both user-designed threshold and Otsu adaptive threshold
    def thresholding(self):
#  two thresholding method, mannual and Otsu       
        
        if self.mode is 'mannual':
            mask = self.image > self.thresh
#            mask = np.copy(self.image)
#            mask.fill(0)            
#            .zeros(np.size(self.image))
#            mask[(self.image>self.thresh).nonzero()]=1
        if self.mode is 'Otsu':
            T = threshold_otsu(self.image)
            mask = self.image > T
            
        return mask
    
    