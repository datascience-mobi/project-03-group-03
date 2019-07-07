# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
Global Otsu thresholding
@author: Luis
"""
import numpy as np
import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte
import skimage.io
import skimage.filters
import dice as dic
import get_im as im
import enhance as enh
import re
import os


def figure_of_original_histogram_and_otsu(axes, binary_original, control_image, match_global, dice_score_global,
                                          sobel_edged_image, original_merge_edge, binary_sobel, original_image):
    """
    A figure is created and shown with 6 subplots for y images
    :param axes: axes for a figure defined in main
    :param binary_original: the optimal value of the threshold is added
    :param control_image: the assembled given control is placed
    :param match_global: the deviation overlay is placed
    :param dice_score_global: a number repesenting the dice score is inserted
    :param sobel_edged_image: the image of sobal edges is placed
    :param original_merge_edge: merge of original and sobal edges is placed
    :param binary_sobel: the original_merge_edge is binarized
    :param original_image: untreated image is placed
    :return:
    """

    axes[0].imshow(original_image, cmap=plt.cm.gray)
    axes[0].set_title('Global Otsu')
    axes[0].axis('off')

    axes[1].imshow(binary_original, cmap=plt.cm.gray)
    axes[1].set_title('Global Otsu')
    axes[1].axis('off')

    axes[2].imshow(control_image, cmap=plt.cm.gray)
    axes[2].set_title('Optimal threshold')
    axes[2].axis('off')

    axes[3].imshow(match_global, cmap=plt.cm.gray)
    axes[3].set_title(f'deviation of global\n {dice_score_global}')
    axes[3].axis('off')

    axes[4].imshow(sobel_edged_image, cmap=plt.cm.gray)
    axes[4].set_title(f'only edges')
    axes[4].axis('off')

    axes[5].imshow(original_merge_edge, cmap=plt.cm.gray)
    axes[5].set_title(f'edge + image ')
    axes[5].axis('off')

    axes[6].imshow(binary_sobel, cmap=plt.cm.gray)
    axes[6].set_title(f'thresh e+i')
    axes[6].axis('off')


def x_axis_plots(axes, match_local, score_increase, radius):
    """

    :param axes: axes for a figure defined in main
    :param match_local: the deviation overlay between control images and local thresholded is placed
    :param score_increase: local - global otsu
    :param radius: the size the locus of local otsu should have
    :return: subplots with match image dice score and colour background depending on in- decrease
    """

    if score_increase > 0:
        c = 'green'
    elif score_increase < 0:
        c = "red"
    else:
        c = "yellow"

    axes[7].imshow(match_local, cmap=plt.cm.gray)
    axes[7].set_title(f'{radius}\n {round(score_increase, 6)}', fontsize=15, bbox=dict(facecolor=c, alpha=1.5))
    axes[7].axis('off')


def figure_of_different_disc_size(image_directory, control_directory):
    """
    created all parameters for figure with imported subplots
    :param image_directory: directory where the images can be found
    :param control_directory: directory where the controls can be found
    :return: a figure with the thresholds of global and optimal and the matches/scores of different radii
    """

    path_list = []
    name_list = []
    global_score_list = []
    # local_score_list = []

    for root, dirs, files in os.walk(image_directory, topdown=False):
        for name in files:
            image_paths = os.path.join(root, name)  # join directory and namr to path

            # image paths fulfilling name_criteria are selected
            name_criteria = "1h 1_c5.TIF"
            length = len(name_criteria)
            if image_paths[-length:] == name_criteria:  # if the last (length) digits fulfill name criteria -> move on
                path_list.append(image_paths)
                name_list.append(name)

    figure, axes = plt.subplots(1, 8, figsize=(30, 10))

    for idx, path in enumerate(path_list, 0):

        print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4] + ".*")
        original_image = im.import_image(path)
        original_image = img_as_ubyte(original_image)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary_original = original_image > thresh_value

        binary_control = im.assemble_and_import_control_image(control_directory, control_search_filter)

        match_global = dic.creation_of_match_array(binary_original, binary_control)

        dice_score_global = dic.dice_score(binary_original, binary_control)

        global_score_list.append(dice_score_global)
        # local_score_list.append(dice_score_local)

        sobel_edged_image = enh.sobel_edge_detection(original_image)
        sobel_edged_filtered_image = enh.median_filter(sobel_edged_image)

        original_merge_edge = np.add(original_image, sobel_edged_filtered_image)

        sobel_thresh_value = skimage.filters.threshold_otsu(original_merge_edge)
        binary_sobel = original_merge_edge > sobel_thresh_value

        figure_of_original_histogram_and_otsu(axes, binary_original, binary_control, match_global, dice_score_global,
                                              sobel_edged_filtered_image, original_merge_edge, binary_sobel,
                                              original_image)

        radius_list = np.array([1])
        for dx, radius in enumerate(radius_list, 6):

            match_gauss = dic.creation_of_match_array(binary_sobel, binary_control)
            dice_score_gauss = dic.dice_score(binary_sobel, binary_control)
            score_increase = dice_score_gauss - dice_score_global
            x_axis_plots(axes, match_gauss, score_increase, radius)

    plt.show()
    total_dice_score = (sum(global_score_list))/len(path_list)
    print('Total dice score: ', total_dice_score)


def main():

    control = 'BBBC020_v1_outlines_nuclei.zip'
    testing = 'BBBC020_v1_images.zip'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = "all images/BBBC020_v1_images/"
    control_directory = "all controls/BBC020_v1_outlines_nuclei/"

    # figure_of_different_disc_size(image_directory, control_directory)

    radius_list = np.array([1])

    path_list = []
    name_list = []
    # global_score_list = []
    global_mean_score_list = []

    for root, dirs, files in os.walk(image_directory, topdown=False):
        for name in files:
            image_paths = os.path.join(root, name)  # join directory and name to path

            # image paths fulfilling name_criteria are selected
            name_criteria = "_c5.TIF"
            length = len(name_criteria)
            if image_paths[-length:] == name_criteria:  # if the last (length) digits fulfill name criteria -> move on
                path_list.append(image_paths)
                name_list.append(name)

    for dx, radius in enumerate(radius_list, 0):
        current_score_list = []
        print(radius)
        for idx, path in enumerate(path_list, 0):

            print(idx, name_list[idx])

            control_search_filter = re.compile(name_list[idx][:-4] + ".*")
            original_image = im.import_image(path)
            # original_image = img_as_ubyte(original_image)
            original_image = enh.median_filter(original_image)
            # thresh_value = skimage.filters.threshold_otsu(original_image)

            sobel_edged_image = enh.sobel_edge_detection(original_image)
            sobel_edged_filtered_image = enh.median_filter(sobel_edged_image)
            original_merge_edge = np.add(original_image, sobel_edged_filtered_image)
            sobel_thresh_value = skimage.filters.threshold_otsu(original_merge_edge)
            binary_sobel = original_merge_edge > sobel_thresh_value

            binary_control = im.assemble_and_import_control_image(control_directory, control_search_filter)

            dice_score_global = dic.dice_score(binary_sobel, binary_control)

            current_score_list.append(dice_score_global)

        global_mean_score_list.append(sum(current_score_list)/len(current_score_list))

    print(global_mean_score_list)

    # radius_list = np.array([1, 2, 3])
    # global_mean_score_list = np.array([0.9, 0.99, 0.98])
    plt.plot(radius_list, global_mean_score_list, 'go-', linewidth=2)
    global_otsu_mean = 0.9847390203373723
    plt.axhline(y=global_otsu_mean, color='r', linestyle='--', linewidth=1, label='Total dice score')
    plt.legend()
    plt.title('sigma dependent dice score')
    plt.xlabel('sigma')
    plt.ylabel('dice score')
    plt.show()


if __name__ == "__main__":
    main()
