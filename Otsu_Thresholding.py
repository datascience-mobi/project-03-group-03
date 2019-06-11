# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
Global Otsu thresholding
@author: Luis
"""

import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.filters import threshold_otsu


def import_image(path, name):
    # data/image is found in directory and imported as gray scale image
    raw_image_directory = path + name
    image = imread(raw_image_directory, as_gray=True)
    return image


def figure(original_image, binary_image, threshold_value):
    # figure is created with 3 subplots in one row but 3 columns
    fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
    ax = axes.ravel()

    # axes 0 is the first subplot of the 1 row/3 column figure at position one
    # it shows the original image in gray scale. Axis labeling is turned off
    ax[0] = plt.subplot(1, 3, 1)
    ax[0].imshow(original_image, cmap=plt.cm.gray)
    ax[0].set_title('Original')
    ax[0].axis('off')

    # Histogram of the normalized intensity distribution is created at position two.
    # A line indicating the Otsu threshold was added
    ax[1] = plt.subplot(1, 3, 2)
    ax[1].hist(original_image.ravel(), bins=256)
    ax[1].set_title('Histogram')
    ax[1].axvline(threshold_value, color='r', label='Threshold Value')
    ax[1].legend()

    # The third subplot is showing the binary image after otsu thresholding. Again the axis labeling is turned off
    ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0])
    ax[2].imshow(binary_image, cmap=plt.cm.gray)
    ax[2].set_title('Thresholded')
    ax[2].axis('off')

    plt.show()
    return


def main():
    # Directory and image were defined
    name = "jw-1h1_c5.TIF"
    path = "C:\\Users\\User\\PycharmProjects\\Otsu_thresholding\\"

    # import function was executed and optimal threshold value is determined by skimage

    image = import_image(path, name)
    thresh = threshold_otsu(image)
    # image is binarized(False = black, True = white) and final figure is created
    binary = image > thresh
    figure(image, binary, thresh)
    # print(binary)


if __name__ == "__main__":
    main()
