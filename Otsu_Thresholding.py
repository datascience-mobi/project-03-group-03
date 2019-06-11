# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
Global Otsu thresholding
@author: Luis
"""

import matplotlib.pyplot as plt
import skimage.io
import skimage.filters


def import_image(path, name):
    # data/image is found in directory and imported as gray scale image
    raw_image_path = path + "\\" + name
    image = skimage.io.imread(raw_image_path, as_gray=True)
    return image


def original_image_axes(original_image):
    # original_image_axes creates the first subplot in the first column of the figure.
    # it shows the original image in gray scale. Axis labeling is turned off
    plt.subplot(1, 3, 1)

    plt.imshow(original_image, cmap=plt.cm.gray)
    plt.title('Original')
    plt.axis('off')


def intensity_histogram(original_image, threshold_value):
    # Histogram of the normalized intensity distribution is created at second column.
    # A line indicating the Otsu threshold was added
    plt.subplot(1, 3, 2)
    plt.hist(original_image.ravel(), bins=256)
    plt.title('Histogram')
    plt.axvline(threshold_value, color='r', label='Threshold Value')
    plt.legend()


def binary_otsu_image(binary_image):
    # The third subplot is showing the binary image after otsu thresholding. Again the axis labeling is turned off
    plt.subplot(1, 3, 3)
    plt.imshow(binary_image, cmap=plt.cm.gray)
    plt.title('Thresholded')
    plt.axis('off')


def figure_of_original_histogram_and_otsu(original_image, binary_image, threshold_value):
    # A figure is created and shown with 3 subplots

    plt.figure(figsize=(8, 2.5))

    original_image_axes(original_image)
    intensity_histogram(original_image, threshold_value)
    binary_otsu_image(binary_image)

    plt.show()


def main():
    # Directory and image were defined
    name = "jw-1h1_c5.TIF"
    path = "C:\\Users\\User\\PycharmProjects\\Otsu_thresholding"

    # import function was executed and optimal threshold value is determined by skimage

    image = import_image(path, name)
    thresh = skimage.filters.threshold_otsu(image)
    # image is binarized(False = black, True = white) and final figure is created
    binary = image > thresh
    figure_of_original_histogram_and_otsu(image, binary, thresh)


if __name__ == "__main__":
    main()
