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
import os


def figure_of_original_histogram_and_otsu(original_image, binary_image, threshold_value, control_directory,
                                          search_filter, name):
    """
    A figure is created and shown with 6 subplots
    :param original_image: untreated image is placed
    :param binary_image: the optimal value of the threshold is added
    :param threshold_value: image after otsu thresholding is placed
    :param control_directory: directory where control images are found
    :param search_filter: name criteria for images contributing to the control image
    :param name: name of original/chose file is added as title
    :return: a figure wuth six subplots original, histogram, thresholded, optimal, matches and dice score
    """

    binary_control = im.assemble_and_import_control_image(control_directory, search_filter)
    control_image = im.assemble_and_import_control_image(control_directory, search_filter)
    match_image = dic.creation_of_match_array(binary_image, binary_control)
    dice_score = dic.dice_score(binary_image, binary_control)
    figure, axes = plt.subplots(3, 2, figsize=(6, 8))

    axes[0][0].imshow(original_image, cmap=plt.cm.gray)
    axes[0][0].set_title('Original: ' + name)
    axes[0][0].axis('off')

    axes[0][1].hist(original_image.ravel(), bins=256)  # TODO ask for normalization/scaling
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
    # name = "jw-1h 5_c5.TIF"  # zB.jw-1h 2_c5.TIF , jw-1h 3_c5.TIF , jw-Kontrolle1_c5.TIF
    # image_directory = "all images\\BBBC020_v1_images\\" + name[:-7]


    # TODO change directory methodology

    control = 'BBBC020_v1_outlines_nuclei.ZIP'
    testing = 'BBBC020_v1_images.ZIP'
    im.create_control_files_if_there_are_no(control)
    im.create_image_files_if_there_are_no(testing)
    # import function was executed and optimal threshold value is determined by skimage


    # figure_of_original_histogram_and_otsu(image, binary, thresh, control_directory, search_filter, name)
    # dic.main(binary, control_directory, search_filter)

    # Directory and image were defined
    # name = re.compile("jw-1h 2_c5.TIF")  # zB.jw-1h 2_c5.TIF , jw-1h 3_c5.TIF , jw-Kontrolle1_c5.TIF
    image_directory = "all images/BBBC020_v1_images/"

    path_list = []
    name_list = []
    score_list = []
    for root, dirs, files in os.walk(image_directory, topdown=False):
        for name in files:
            image_paths = os.path.join(root, name)
            if image_paths[-7:] == "_c5.TIF":
                path_list.append(image_paths)
                name_list.append(name)
    figure, axes = plt.subplots(25, 6, figsize=(20, 80))

    for idx, path in enumerate(path_list, 0):
        # print(idx, path)
        print(idx, name_list[idx])

        search_filter = re.compile(name_list[idx][:-4]+".*")
        original_image = im.import_image(path)
        thresh = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary = original_image > thresh
        control_directory = "all controls/BBC020_v1_outlines_nuclei/"
        binary_control = im.assemble_and_import_control_image(control_directory, search_filter)
        control_image = im.assemble_and_import_control_image(control_directory, search_filter)
        match_image = dic.creation_of_match_array(binary, binary_control)
        dice_score = dic.dice_score(binary, binary_control)
        score_list.append(dice_score)
        axes[idx][0].imshow(original_image, cmap=plt.cm.gray)
        axes[idx][0].set_title('Original: ' + name_list[idx])
        axes[idx][0].axis('off')

        axes[idx][1].hist(original_image.ravel(), bins=256)  # TODO ask for normalization/scaling
        axes[idx][1].set_title('Intensity Histogram')
        axes[idx][1].axvline(thresh, color='r', label='Threshold Value')
        axes[idx][1].legend()

        axes[idx][2].imshow(binary, cmap=plt.cm.gray)
        axes[idx][2].set_title('Otsu thresh')
        axes[idx][2].axis('off')

        axes[idx][3].imshow(control_image, cmap=plt.cm.gray)
        axes[idx][3].set_title('Optimal threshold')
        axes[idx][3].axis('off')

        axes[idx][4].imshow(match_image, cmap=plt.cm.gray)
        axes[idx][4].set_title('deviation in black')
        axes[idx][4].axis('off')

        axes[idx][5].text(0, 0.5, dice_score)  # TODO ugly, make nice
        axes[idx][5].axis('off')

    plt.show()
    # print(idx)
    # print(score_list)
    total_dice_score = (sum(score_list))/(idx+1)
    print(total_dice_score)


if __name__ == "__main__":
    main()
