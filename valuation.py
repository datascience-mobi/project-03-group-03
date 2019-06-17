# -*- coding: utf-8 -*-
"""
Created on Sat June  15 11:08:50 2019
valuation of Otsu thresholding
@author: Luis
"""

import matplotlib.pyplot as plt
import skimage.io
import skimage.filters
import re
import os
import numpy as np


def assemble_and_import_control_image(directory, name):
    # A blank image - consisting of black pixels/zeros- is created
    blank_image_to_add_to = np.zeros((1040, 1388))

    # For loop walks through a given directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if name.match(file):
                # It imports all files matching the name-criteria and adds them to the blank
                image = skimage.io.imread(directory + "\\" + file, as_gray=True)
                blank_image_to_add_to = np.add(blank_image_to_add_to, image)

    binary_image = blank_image_to_add_to > 100
    return binary_image


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
    plt.subplot()
    plt.imshow(binary_image, cmap=plt.cm.gray)
    plt.axis('off')


def dice_coefficient(binary_image, binary_control):

    control = binary_control
    image = binary_image
    match = np.array(control == image)
    return match


def figure_of_control(binary_image):
    # A figure is created and shown with 3 subplots

    plt.figure(figsize=(3, 3))
    binary_otsu_image(binary_image)
    plt.show()

def main():
    # Directory where the sub-controle
    directory = "C:\\Users\\User\\Documents\\GitHub\\project-03-group-03\\BBC020_v1_outlines_nuclei"
    # scuht nach allem in der klammer

    blank_image_to_add_t = np.zeros((1040, 1388))
    image = blank_image_to_add_t > 100
    search_filter = re.compile(".*1h 1.*")

    control_image = assemble_and_import_control_image(directory, search_filter)

    # figure_of_control(control_image)
    match = dice_coefficient(image, control_image)
    # figure_of_control(match)
    true = sum(sum(match))
    false = np.size(match) - true
    dice_score = 2*true/(2*true+false)
    print("True hits ", true)
    print("False hits ", false)
    print("Dice score ", dice_score)

if __name__ == "__main__":
    main()


