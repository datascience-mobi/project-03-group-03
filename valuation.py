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

control_directory = "C:\\Users\\User\\Documents\\GitHub\\project-03-group-03\\BBC020_v1_outlines_nuclei"

search_filter = re.compile(".*1h 1.*")
# filter for name criteria. TODO link to analized image. valuation shouldn't be touched.


def assemble_and_import_control_image(directory, name):
    # A blank image - consisting of black pixels/zeros- is created. It serves as a base to add all images to.
    blank_image_to_add_to = np.zeros((1040, 1388))

    # For loop walks through a given directory and takes all names fulfilling the criteria.
    # TODO try something without for loop.
    for root, dirs, files in os.walk(directory):
        for file in files:
            if name.match(file):
                # It imports all files matching the name-criteria and adds them to the blank.
                image = skimage.io.imread(directory + "\\" + file, as_gray=True)
                blank_image_to_add_to = np.add(blank_image_to_add_to, image)

    # Final image with all nuclei added is binarized into an True False np array.
    binary_image = blank_image_to_add_to > 100
    return binary_image


def creation_of_match_array(binary_image, binary_control):
    # Function compares two arrays and returns an array where differences are set False and matches True.
    control = binary_control
    image = binary_image
    match = np.array(control == image)
    return match


def dice_score(binary_original, binary_control):
    # counts matches and deviations
    # figure_of_control(binary_control, 'Optimal given threshold')
    match = creation_of_match_array(binary_original, binary_control)
    # figure_of_control(match, 'deviation of optimal threshold and otsu')
    true = sum(sum(match))
    false = np.size(match) - true
    score = 2 * true / (2 * true + false)
    print("True hits: ", true)
    print("False hits: ", false)
    print("Dice score: ", score)


# def binary_otsu_image(binary_image, title):
#    # The third subplot is showing the binary image after otsu thresholding. Again the axis labeling is turned off
#    plt.subplot()
#    plt.imshow(binary_image, cmap=plt.cm.gray)
#    plt.title(title)
#    plt.axis('off')


# def figure_of_control(binary_image, title):
    # A figure is created and shown with 3 subplots

#    plt.figure(figsize=(3, 3.2))
#    binary_otsu_image(binary_image, title)
#    plt.show()


def creation_of_control_image_subplot():
    # creation of subplot for optimal threshold
    control_image = assemble_and_import_control_image(control_directory, search_filter)
    plt.subplot(2, 3, 4)
    plt.imshow(control_image, cmap=plt.cm.gray)
    plt.title('optimal thresh')
    plt.axis('off')


def creation_of_match_subplot(binary_original):
    # creation of subplot for matches
    control_image = assemble_and_import_control_image(control_directory, search_filter)
    match = creation_of_match_array(binary_original, control_image)
    plt.subplot(2, 3, 5)
    plt.imshow(match, cmap=plt.cm.gray)
    plt.title('deviation in black')
    plt.axis('off')


def main(image):

    control_image = assemble_and_import_control_image(control_directory, search_filter)

    dice_score(image, control_image)


if __name__ == "__main__":
    main()
