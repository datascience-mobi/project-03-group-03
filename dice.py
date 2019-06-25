# -*- coding: utf-8 -*-
"""
Created on Sat June  15 11:08:50 2019
valuation of Otsu thresholding
@author: Luis
"""

import get_im as im
import numpy as np


def creation_of_match_array(binary_image, binary_control):
    """
    Function compares two arrays and returns an array where differences are set False and matches True.
    :param binary_image: image that was binarized due to the threshold value
    :param binary_control: the control image assembled out of given data
    :return: image/array of deviations between otzu and the given optimum(match in white deviation in black)
    """
    control = binary_control
    image = binary_image
    match = np.array(control == image)
    return match


def dice_score(binary_image, binary_control):
    """
    counts matches and deviations
    :param binary_image: image that was binarized due to the threshold value
    :param binary_control: the control image assembled out of given data
    :return: a number representing the percentage of right assigned pixels
    """
    # figure_of_control(binary_control, 'Optimal given threshold')
    match = creation_of_match_array(binary_image, binary_control)
    # figure_of_control(match, 'deviation of optimal threshold and otsu')
    true = sum(sum(match))
    false = np.size(match) - true
    score = 2 * true / (2 * true + false)
    #print("True hits: ", true)
    #print("False hits: ", false)
    print("Dice score: ", score)
    return 'Dice score: ', score


def dice_calculation(image, control_directory, search_filter):

    # control_image = im.assemble_and_import_control_image(control_directory, search_filter)
    # dice_score(image, control_image)
    pass


def main(image, control_directory, search_filter):
    # control_directory = "C:\\Users\\User\\Documents\\GitHub\\project-03-group-03\\BBC020_v1_outlines_nuclei"
    control_image = im.assemble_and_import_control_image(control_directory, search_filter)

    dice_score(image, control_image)


if __name__ == "__main__":
    main()
