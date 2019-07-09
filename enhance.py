# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
local otsu
@author: Luis
"""

import skimage as sk
from skimage.morphology import disk
from skimage.filters import rank
from skimage.util import img_as_ubyte


def local_otsu(image, radius):
    """

    :param image: input image(original)
    :param radius: size of disc- shaped mask for local otsu
    :return: local thresholded image (and maybe the mask)
    """

    img = img_as_ubyte(image)

    selem = disk(radius)

    local_otsu_mask = rank.otsu(img, selem)
    local_thresholded_image = img > local_otsu_mask

    return local_thresholded_image


def gaussian_filter(image_path, sigma):
    """

    :param image_path: input image(original)
    :param sigma: definition of width of gaussian distribution in mask
    :return: a filtered/smoothed image
    """

    img = img_as_ubyte(image_path)

    gauss_image = sk.filters.gaussian(img, sigma=sigma)
    return gauss_image


def median_filter(image_path):
    """

    :param image_path: input image(original)
    :return: a filtered/smoothed image
    """

    img = img_as_ubyte(image_path)

    median_image = sk.filters.median(img)
    return median_image


def sobel_edge_detection(image_path):
    """

    :param image_path: input image(original)
    :return: a image with highlighted edges of input_image
    """

    img = img_as_ubyte(image_path)

    sobel_image = sk.filters.sobel(img)
    return sobel_image


def colour_indication(score_increase):
    """

    :param score_increase: a number being >, < or = 0
    :return: a colour regarding the sign
    """

    if score_increase > 0:  # TODO modularize
        colour = 'green'
    elif score_increase < 0:
        colour = 'red'
    else:
        colour = 'yellow'

    return colour
