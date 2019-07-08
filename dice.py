# -*- coding: utf-8 -*-
"""
Created on Sat June  15 11:08:50 2019
valuation of Otsu thresholding
@author: Luis
"""

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
    # print("True hits: ", true)
    # print("False hits: ", false)
    print('Dice score: ', score)
    return score
