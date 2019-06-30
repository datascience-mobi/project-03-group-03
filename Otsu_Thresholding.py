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


def figure_of_original_histogram_and_otsu(axes, y, original_image, binary_original, thresh_value, control_image,
                                          name, match_image, dice_score):
    """
    A figure is created and shown with 6 subplots for y images
    :param axes: axes for a figure defined in main
    :param y: vertical position of axes in figure
    :param original_image: untreated image is placed
    :param binary_original: the optimal value of the threshold is added
    :param thresh_value: image after otsu thresholding is placed
    :param control_image: the assembled given control is placed
    :param name: the name of the seached image
    :param match_image: the deviation overlay is placed
    :param dice_score: a number repesenting the dice score is inserted
    :return: six subplots original, histogram, thresholded, optimal, matches and dice score without a figure
    """

    axes[y][0].imshow(original_image, cmap=plt.cm.gray)
    axes[y][0].set_title('Original: ' + name)
    axes[y][0].axis('off')

    axes[y][1].hist(original_image.ravel(), bins=256)
    axes[y][1].set_title('Intensity Histogram')
    axes[y][1].axvline(thresh_value, color='r', label='Threshold Value')
    axes[y][1].legend()

    axes[y][2].imshow(binary_original, cmap=plt.cm.gray)
    axes[y][2].set_title('Global Otsu')
    axes[y][2].axis('off')

    axes[y][3].imshow(control_image, cmap=plt.cm.gray)
    axes[y][3].set_title('Optimal threshold')
    axes[y][3].axis('off')

    axes[y][4].imshow(match_image, cmap=plt.cm.gray)
    axes[y][4].set_title('deviation in black')
    axes[y][4].axis('off')

    axes[y][5].text(0, 0.5, dice_score)  # TODO still ugly, make nice
    axes[y][5].axis('off')


def main():

    control = 'BBBC020_v1_outlines_nuclei.ZIP'
    testing = 'BBBC020_v1_images.ZIP'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = "all images/BBBC020_v1_images/"

    path_list = []
    name_list = []
    score_list = []

    for root, dirs, files in os.walk(image_directory, topdown=False):
        for name in files:
            image_paths = os.path.join(root, name)  # join directory and namr to path

            # image paths fulfilling name_criteria are selected
            name_criteria = "_c5.TIF"
            length = len(name_criteria)
            if image_paths[-length:] == name_criteria:  # if the last (length) digits fulfill name criteria -> move on
                path_list.append(image_paths)
                name_list.append(name)

    figure, axes = plt.subplots(25, 6, figsize=(20, 80))

    for idx, path in enumerate(path_list, 0):
        print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4]+".*")
        original_image = im.import_image(path)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary_original = original_image > thresh_value
        control_directory = "all controls/BBC020_v1_outlines_nuclei/"
        binary_control = im.assemble_and_import_control_image(control_directory, control_search_filter)
        match_image = dic.creation_of_match_array(binary_original, binary_control)
        dice_score = dic.dice_score(binary_original, binary_control)
        score_list.append(dice_score)
        figure_of_original_histogram_and_otsu(axes, idx, original_image, binary_original, thresh_value, binary_control,
                                              name_list[idx], match_image, dice_score)

    plt.show()
    total_dice_score = (sum(score_list))/(idx+1)
    print('Total dice score: ', total_dice_score)


if __name__ == "__main__":
    main()
