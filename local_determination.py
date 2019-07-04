# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
Global Otsu thresholding
@author: Luis
"""
import numpy as np
import matplotlib.pyplot as plt
import skimage.io
import skimage.filters
import dice as dic
import get_im as im
import local_otsu as loco
import re
import os


def figure_of_original_histogram_and_otsu(axes, binary_original, control_image, match_global, dice_score_global):
    """
    A figure is created and shown with 6 subplots for y images
    :param axes: axes for a figure defined in main
    :param y: vertical position of axes in figure
    :param original_image: untreated image is placed
    :param binary_original: the optimal value of the threshold is added
    :param thresh_value: image after otsu thresholding is placed
    :param control_image: the assembled given control is placed
    :param name: the name of the seached image
    :param match_global: the deviation overlay is placed
    :param dice_score_global: a number repesenting the dice score is inserted
    :return: six subplots original, histogram, thresholded, optimal, matches and dice score without a figure
    """

    axes[0].imshow(binary_original, cmap=plt.cm.gray)
    axes[0].set_title('Global Otsu')
    axes[0].axis('off')

    axes[1].imshow(control_image, cmap=plt.cm.gray)
    axes[1].set_title('Optimal threshold')
    axes[1].axis('off')

    axes[2].imshow(match_global, cmap=plt.cm.gray)
    axes[2].set_title(f'deviation of global\n {dice_score_global}')
    axes[2].axis('off')


def x_axis_plots(axes, y, x, match_local, score_increase, radius):

    if score_increase > 0:
        c = 'green'
    elif score_increase < 0:
        c = "red"
    else:
        c = "yellow"

    axes[x].imshow(match_local, cmap=plt.cm.gray)
    axes[x].set_title(f'{radius}\n {round(score_increase, 6)}'
                         , fontsize=15, bbox=dict(facecolor=c, alpha=1.5))
    axes[x].axis('off')


def figure_of_different_disc_size():

    control = 'BBBC020_v1_outlines_nuclei.ZIP'
    testing = 'BBBC020_v1_images.ZIP'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = "all images/BBBC020_v1_images/"

    path_list = []
    name_list = []
    global_score_list = []
    # local_score_list = []

    for root, dirs, files in os.walk(image_directory, topdown=False):
        for name in files:
            image_paths = os.path.join(root, name)  # join directory and namr to path

            # image paths fulfilling name_criteria are selected
            name_criteria = "24h 1_c5.TIF"
            length = len(name_criteria)
            if image_paths[-length:] == name_criteria:  # if the last (length) digits fulfill name criteria -> move on
                path_list.append(image_paths)
                name_list.append(name)

    figure, axes = plt.subplots(1, 7, figsize=(30, 10))

    for idx, path in enumerate(path_list, 0):

        print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4] + ".*")
        original_image = im.import_image(path)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary_original = original_image > thresh_value
        control_directory = "all controls/BBC020_v1_outlines_nuclei/"
        binary_control = im.assemble_and_import_control_image(control_directory, control_search_filter)

        match_global = dic.creation_of_match_array(binary_original, binary_control)

        dice_score_global = dic.dice_score(binary_original, binary_control)

        global_score_list.append(dice_score_global)
        # local_score_list.append(dice_score_local)

        figure_of_original_histogram_and_otsu(axes, binary_original, binary_control, match_global,
                                              dice_score_global)

        radius_list = [5, 20, 50, 200]
        for dx, radius in enumerate(radius_list, 3):
            local_otsu = loco.local_otsu(original_image, radius)
            match_local = dic.creation_of_match_array(local_otsu, binary_control)
            dice_score_local = dic.dice_score(local_otsu, binary_control)
            score_increase = dice_score_local - dice_score_global
            x_axis_plots(axes, idx, dx, match_local, score_increase, radius)

    plt.show()
    # total_dice_score = (sum(global_score_list))/len(path_list)
    # print('Total dice score: ', total_dice_score)


def main():

    figure_of_different_disc_size()
    radius_list = np.append([5], np.arange(10, 200, 10))

    control = 'BBBC020_v1_outlines_nuclei.ZIP'
    testing = 'BBBC020_v1_images.ZIP'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = "all images/BBBC020_v1_images/"

    path_list = []
    name_list = []
    # global_score_list = []
    # local_mean_score_list = []

    for root, dirs, files in os.walk(image_directory, topdown=False):
        for name in files:
            image_paths = os.path.join(root, name)  # join directory and namr to path

            # image paths fulfilling name_criteria are selected
            name_criteria = "1_c5.TIF"
            length = len(name_criteria)
            if image_paths[-length:] == name_criteria:  # if the last (length) digits fulfill name criteria -> move on
                path_list.append(image_paths)
                name_list.append(name)
    local_mean_score_list = []
    for dx, radius in enumerate(radius_list, 0):
        current_score_list = []
        for idx, path in enumerate(path_list, 0):

            print(idx, name_list[idx])

            control_search_filter = re.compile(name_list[idx][:-4] + ".*")
            original_image = im.import_image(path)

            control_directory = "all controls/BBC020_v1_outlines_nuclei/"
            binary_control = im.assemble_and_import_control_image(control_directory, control_search_filter)
            local_otsu = loco.local_otsu(original_image, radius)

            dice_score_local = dic.dice_score(local_otsu, binary_control)

            current_score_list.append(dice_score_local)

        local_mean_score_list.append(sum(current_score_list)/len(current_score_list))
    plt.show()

    print(local_mean_score_list)
    plt.plot(radius_list, local_mean_score_list)
    plt.show()


if __name__ == "__main__":
    main()
