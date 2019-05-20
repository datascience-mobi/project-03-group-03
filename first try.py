# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
first try
@author: mostly Luis
"""

import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt

def raw():
    #defining the image and where to find it
    Name = ( "blood.jpg")
    Path = ("C:\\Users\\User\\Desktop\\Uni\\inkscape\\")    
    return Name, Path

def img_h(path, name):
    #convert immage to 8 bit grayscale for the histogram
    return Image.open (path + name).convert('L')
    
def img_o(path, name):
    #convert immage to 8 bit grayscale for Thresholding
    return cv2.imread ((path + name), 0)

def ary():
    # creating the histogram with bin range 256 
    Name, Path = raw()
    
    img1 = img_h(Path, Name)
    
    a = np.array(img1.getdata())
    fig, ax = plt.subplots(figsize=(10,5))
    n,bins,patches = ax.hist(a, bins=range(256))
    ax.set_title("histogram ")
    ax.set_xlim(-5,260)
    for b,p in zip(bins,patches):
        p.set_facecolor('r')
    plot = plt.show()
    return plot 
    
def main():    
    #ploting the histogram
    ary()
    img = img_o(raw()[1], raw()[0])
    thv = 0 

    #otsu thresholding using cv2 lib
    ret,thresh1 = cv2.threshold(img,thv,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU )
    ret,thresh2 = cv2.threshold(img,thv,255,cv2.THRESH_TOZERO_INV + cv2.THRESH_OTSU )

    #plotting the original, the binary and the >thresh to 0 images in one figure
    images = [img, thresh1, thresh2]

    titles = ['Original Image', 'BINARY', 'TOZERO_INV']

    for i in range(3):
        plt.subplot(1,3,i+1)
        plt.imshow(images[i], cmap='gray')
        plt.title(titles[i])
        plt.xticks([])
        plt.yticks([])
    plt.savefig('Thresh.png', dpi = 500)    
    plt.show()


if __name__== "__main__":
    main()
