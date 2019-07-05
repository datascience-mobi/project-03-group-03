# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
local otsu
@author: Luis
"""

from skimage.morphology import disk
from skimage.filters import  rank
from skimage.util import img_as_ubyte
import matplotlib

matplotlib.rcParams['font.size'] = 9


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
