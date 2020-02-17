# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 12:57:27 2018

@author: hollie_min
"""

# For Microscope image

import numpy as np
import javabridge as jv
import bioformats as bf
import matplotlib.pyplot as plt
from Microscope_imreader import MC_image_reader
from Basic_processing_functions import Basic_processing
# load the microscope image

jv.start_vm(class_path=bf.JARS,max_heap_size='4G')

impath = 'C:\work\Microscopy\image\HeLa_R-CIM6PR-488, G-VPS35-555, M-EEA1-647_R1.lif'
F = MC_image_reader(impath)
image = bf.load_image(impath)

# basic image processing
# 1,histogram equalization
#image.max()
#image.min()
hist,bin_edges  = np.histogram(image[:,:,0],bins = 64)
fig = plt.figure()
plt.hist(image[:,:,0].ravel(), bins=256)
proc_image = Basic_processing()
proc_image.mode = 'CLAHE'
proc_image.image = image[:,:,0]
proc_image.clip_limit = 0.01
proc_image.nbins = 256
eq_image = proc_image.histogram_equalization()
#histogram_equalization(image[:,:,1],'CLAHE')
fig = plt.figure()
plt.imshow(eq_image)
# 2, thresholding
proc_image.image = eq_image
proc_image.mode = 'Otsu'
#proc_image.thresh = 0.3
mask = proc_image.thresholding()
fig = plt.figure()
plt.imshow(mask)
#plt.hist(image[:,:,1], 256,normed=1, facecolor='green', alpha=0.75)  # arguments are passed to np.histogram
#plt.title("Histogram with 'auto' bins")
#plt.show()
#jv.kill_vm() this line can only be excuted when you want to close the platform



#plt.figure(0)
#plt.subplot(221)
#plt.imshow(image[:,:,0])
#plt.subplot(222)
#plt.imshow(image[:,:,1])
#plt.subplot(223)
#plt.imshow(image[:,:,2])
#plt.subplot(224)
#plt.imshow(image[:,:,3])