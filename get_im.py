# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
Global Otsu thresholding
@author: Luis
"""

import numpy as np
import skimage.io
import skimage.filters
import zipfile
import os


def import_image(path):
    """
    data/image is found in directory and imported as gray scale image
    :param path: path where image can be found.
    :return: the image that is examined
    """
    raw_image_path = path
    image = skimage.io.imread(raw_image_path, as_gray=True)
    return image


def assemble_and_import_control_image(directory, name):
    """
    A blank image - consisting of black pixels/zeros- is created. It serves as a base to add all images to.
    For loop walks through a given directory and takes all names fulfilling the criteria.
    It imports all files matching the name-criteria and adds them to the blank.
    Final image with all nuclei added is binarized into an True False np array.
    :param directory: the directory where the loop is searching for the name (criteria)
    :param name: the name that is searched for eache cycle
    :return: an image of all assembled images being thresholded/binarized
    """
    #
    blank_image_to_add_to = np.zeros((1040, 1388))
    #
    for root, dirs, files in os.walk(directory):
        for file in files:
            if name.match(file):
                image = skimage.io.imread(directory + "/" + file, as_gray=True)
                blank_image_to_add_to = np.add(blank_image_to_add_to, image)

    binary_image = blank_image_to_add_to > 100
    return binary_image


def create_unzipped_files_if_there_are_no(zipped, title):
    """
    checking if unzipped images were already created im working directory.
    If not, it unzippes and creates it.
    :param zipped: an folder or file that needs to be absent to trigger this function
    :param title: name of folder which is looked for or created
    :return: an folder with unzipped images
    """

    cwd = os.getcwd()  # current working directory is taken
    existing = os.path.exists(cwd + '/' + title)

    if not existing:
        zf = zipfile.ZipFile(zipped, 'r')
        zf.extractall(title)
        print('created', title, 'folder')
