# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
Global Otsu thresholding
@author: Luis
"""

import matplotlib.pyplot as plt
import skimage.io
import skimage.filters
import dice as dic
import get_im as im
import re


def original_image_axes(original_image):
    # original_image_axes creates the first subplot in the first column of the figure.
    # it shows the original image in gray scale. Axis labeling is turned off
    plt.subplot(2, 3, 1)

    plt.imshow(original_image, cmap=plt.cm.gray)
    plt.title('Original')
    plt.axis('off')


def intensity_histogram(original_image, threshold_value):
    # Histogram of the normalized intensity distribution is created at second column.
    # A line indicating the Otsu threshold was added
    plt.subplot(2, 3, 2)
    plt.hist(original_image.ravel(), bins=256)
    plt.title('Histogram')
    plt.axvline(threshold_value, color='r', label='Threshold Value')
    plt.legend()


def binary_otsu_image(binary_image):
    # The third subplot is showing the binary image after otsu thresholding. Again the axis labeling is turned off
    plt.subplot(2, 3, 3)
    plt.imshow(binary_image, cmap=plt.cm.gray)
    plt.title('Otsu thresh')
    plt.axis('off')


def figure_of_original_histogram_and_otsu(original_image, binary_image, threshold_value):
    # A figure is created and shown with 3 subplots TODO ask how this figure creation works.
    plt.figure(figsize=(8, 3.2))
    original_image_axes(original_image)
    intensity_histogram(original_image, threshold_value)
    binary_otsu_image(binary_image)
    # implementation of validation plots TODO link to main/ ask how it can be done.
    val.creation_of_control_image_subplot()
    val.creation_of_match_subplot(binary_image)

    plt.show()


def main():
    # Directory and image were defined
    name = "jw-1h1_c5.TIF"
    path = "C:\\Users\\User\\PycharmProjects\\Otsu_thresholding"

    # import function was executed and optimal threshold value is determined by skimage

    image = im.import_image(image_path, name)
    thresh = skimage.filters.threshold_otsu(image)
    # image is binarized(False = black, True = white) and final figure is created
    binary = image > thresh
    figure_of_original_histogram_and_otsu(image, binary, thresh)
    val.main(binary)


if __name__ == "__main__":
    main()
