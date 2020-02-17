# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 16:59:13 2018

@author: hollie_min
"""

# This is a module showing the images from different channel of a microscope image

import matplotlib.pyplot as plt
#import numpy as np
import bioformats as bf

def MC_image_reader(image_path):
    image = bf.load_image(image_path)
#    fig,axs = plt.subplots(nrows=2,ncols=2)#4 channels
    fig = plt.figure()
    plt.subplot(221)
    plt.imshow(image[:,:,0])
    plt.subplot(222)
    plt.imshow(image[:,:,1])
    plt.subplot(223)
    plt.imshow(image[:,:,2])
    plt.subplot(224)
    plt.imshow(image[:,:,3])
    
    return fig