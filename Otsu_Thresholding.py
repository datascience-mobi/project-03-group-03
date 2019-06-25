## -*- coding: utf-8 -*-
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


def figure_of_original_histogram_and_otsu\
                (original_image, binary_image, threshold_value, control_directory, search_filter, name):
    """
    A figure is created and shown with 6 subplots
    :param original_image: image is shown
    :param binary_image:
    :param threshold_value:
    :param control_directory:
    :param search_filter:
    :return:
    """

    binary_control = im.assemble_and_import_control_image(control_directory, search_filter)
    control_image = im.assemble_and_import_control_image(control_directory, search_filter)
    match_image = dic.creation_of_match_array(binary_image, binary_control)
    dice_score = dic.dice_score(binary_image, binary_control)
    figure, axes = plt.subplots(3, 2, figsize=(6, 8))

    axes[0][0].imshow(original_image, cmap=plt.cm.gray)
    axes[0][0].set_title('Original: ' + name)
    axes[0][0].axis('off')

    axes[0][1].hist(original_image.ravel(), bins=256)
    axes[0][1].set_title('Intensity Histogram')
    axes[0][1].axvline(threshold_value, color='r', label='Threshold Value')
    axes[0][1].legend()

    axes[1][0].imshow(binary_image, cmap=plt.cm.gray)
    axes[1][0].set_title('Otsu thresh')
    axes[1][0].axis('off')

    axes[1][1].imshow(control_image, cmap=plt.cm.gray)
    axes[1][1].set_title('Optimal threshold')
    axes[1][1].axis('off')

    axes[2][0].imshow(match_image, cmap=plt.cm.gray)
    axes[2][0].set_title('deviation in black')
    axes[2][0].axis('off')

    axes[2][1].text(0, 0.5,  dice_score)  # TODO ugly, make nice
    axes[2][1].axis('off')

    plt.show()


def main():

    # Directory and image were defined
    name = "jw-1h 1_c5.TIF"  # zB.jw-1h 2_c5.TIF , jw-1h 3_c5.TIF , jw-Kontrolle1_c5.TIF
    image_path = "all images\\BBBC020_v1_images\\" + name[:-7]
    control_path = "all controls\\BBC020_v1_outlines_nuclei\\"
    search_filter = re.compile(name[:-4]+".*")
    control = 'BBBC020_v1_outlines_nuclei.ZIP'
    testing = 'BBBC020_v1_images.ZIP'
    im.create_control_files_if_there_are_no(control)
    im.create_image_files_if_there_are_no(testing)
    # import function was executed and optimal threshold value is determined by skimage

    image = im.import_image(image_path, name)
    thresh = skimage.filters.threshold_otsu(image)
    # image is binarized(False = black, True = white) and final figure is created
    binary = image > thresh
    figure_of_original_histogram_and_otsu(image, binary, thresh, control_path, search_filter, name)
    #dic.main(binary, control_path, search_filter)



if __name__ == "__main__":
    main()