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


def figure_of_original_edges_and_otsu(axes, binary_original, control_image, match_global, dice_score_global,
                                      sobel_edged_image, original_merge_edge, binary_sobel, original_image,
                                      match_local, score_increase):
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
    :param match_local: the deviation overlay between control images and local thresholded is placed
    :param score_increase: local - global otsu
    :return:
    """

    axes[0][0].imshow(original_image, cmap=plt.cm.gray)
    axes[0][0].set_title('Original', fontsize=19)
    axes[0][0].axis('off')

    axes[0][1].imshow(binary_original, cmap=plt.cm.gray)
    axes[0][1].set_title('Global Otsu', fontsize=19)
    axes[0][1].axis('off')

    axes[0][2].imshow(control_image, cmap=plt.cm.gray)
    axes[0][2].set_title('Ground Truth', fontsize=19)
    axes[0][2].axis('off')

    axes[0][3].imshow(match_global, cmap=plt.cm.gray)
    axes[0][3].set_title(f'Deviation with Global\n {dice_score_global}', fontsize=19)
    axes[0][3].axis('off')

    axes[1][0].imshow(sobel_edged_image, cmap=plt.cm.gray)
    axes[1][0].set_title(f'Edges', fontsize=19)
    axes[1][0].axis('off')

    axes[1][1].imshow(original_merge_edge, cmap=plt.cm.gray)
    axes[1][1].set_title(f'Edge + Image ', fontsize=19)
    axes[1][1].axis('off')

    axes[1][2].imshow(binary_sobel, cmap=plt.cm.gray)
    axes[1][2].set_title(f'Thresh E+I', fontsize=19)
    axes[1][2].axis('off')

    colour = enh.colour_indication(score_increase)

    axes[1][3].imshow(match_local, cmap=plt.cm.gray)
    axes[1][3].set_title(f'Dice score Increase: \n{round(score_increase, 6)}', fontsize=19, bbox=dict(facecolor=colour,
                                                                                                      alpha=1.5))
    axes[1][3].axis('off')


def figure_of_different_disc_size(image_directory, control_directory):
    """
    created all parameters for figure with imported subplots
    :param image_directory: directory where the images can be found
    :param control_directory: directory where the controls can be found
    :return: a figure with the thresholds of global and optimal and the matches/scores of different radii
    """

    global_score_list = []
    # local_score_list = []

    path_list, name_list = im.image_path_name_list(image_directory, '24h 3_c5.TIF')

    figure, axes = plt.subplots(2, 4, figsize=(30, 10))

    for idx, path in enumerate(path_list, 0):
        # print(idx, name_list[idx])
        control_search_filter = re.compile(name_list[idx][:-4] + '.*')
        original_image = im.import_image(path)
        original_image = img_as_ubyte(original_image)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        binary_original = original_image > thresh_value

        binary_control, nucleus_count = im.assemble_import_control_image(control_directory, control_search_filter)

        match_global = dic.creation_of_match_array(binary_original, binary_control)
        dice_score_global = dic.dice_score(binary_original, binary_control)

        global_score_list.append(dice_score_global)

        sobel_edged_image = enh.sobel_edge_detection(original_image)
        sobel_edged_filtered_image = enh.median_filter(sobel_edged_image)

        original_merge_edge = np.add(original_image, sobel_edged_filtered_image)

        sobel_thresh_value = skimage.filters.threshold_otsu(original_merge_edge)
        binary_sobel = original_merge_edge > sobel_thresh_value

        match_gauss = dic.creation_of_match_array(binary_sobel, binary_control)
        dice_score_gauss = dic.dice_score(binary_sobel, binary_control)
        score_increase = dice_score_gauss - dice_score_global
        figure_of_original_edges_and_otsu(axes, binary_original, binary_control, match_global, dice_score_global,
                                          sobel_edged_filtered_image, original_merge_edge, binary_sobel,
                                          original_image, match_gauss, score_increase)

    plt.show()


def increase_add_edge():

    control = 'BBBC020_v1_outlines_nuclei.zip'
    testing = 'BBBC020_v1_images.zip'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = 'all images/BBBC020_v1_images/'
    control_directory = 'all controls/BBC020_v1_outlines_nuclei/'

    figure_of_different_disc_size(image_directory, control_directory)

    mean_score_after_edging = []

    path_list, name_list = im.image_path_name_list(image_directory, '_c5.TIF')

    current_score_list = []
    for idx, path in enumerate(path_list):

        # print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4] + '.*')
        original_image = im.import_image(path)
        # original_image = img_as_ubyte(original_image)
        original_image = enh.median_filter(original_image)
        # thresh_value = skimage.filters.threshold_otsu(original_image)

        sobel_edged_image = enh.sobel_edge_detection(original_image)
        sobel_edged_filtered_image = enh.median_filter(sobel_edged_image)
        original_merge_edge = np.add(original_image, sobel_edged_filtered_image)
        sobel_thresh_value = skimage.filters.threshold_otsu(original_merge_edge)
        binary_sobel = original_merge_edge > sobel_thresh_value

        binary_control, counter = im.assemble_import_control_image(control_directory, control_search_filter)

        dice_score_global = dic.dice_score(binary_sobel, binary_control)

        current_score_list.append(dice_score_global)

    mean_score_after_edging.append(sum(current_score_list)/len(current_score_list))

    print('Dice score mean after overlaying the edges is ', mean_score_after_edging[0])

    # radius_list = np.array([1, 2, 3])
    # mean_score_after_edging = np.array([0.9, 0.99, 0.98])
    global_otsu_mean = 0.9847390203373723  # as list for compatibility with mean score afteredging
    score_increase = mean_score_after_edging[0]-global_otsu_mean
    print('Average global Dice score : ', global_otsu_mean)
    print('Increase: ', score_increase)


# if __name__ == '__main__':
    # increase_add_edge()

# filtering


def axes_otsu_filter_masks(axes, binary_original, control_image, match_global, dice_score_global):
    """
    A figure is created and shown with 6 subplots for y images
    :param axes: axes for a figure defined in main
    :param binary_original: the optimal value of the threshold is added
    :param control_image: the assembled given control is placed
    :param match_global: the deviation overlay is placed
    :param dice_score_global: a number representing the dice score is inserted
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


def x_axis_masks(axes, x, match_local, score_increase, radius):
    """

    :param axes: axes for a figure defined in main
    :param x: horizontal position of axes in figure
    :param match_local: the deviation overlay between control images and local thresholded is placed
    :param score_increase: local - global otsu
    :param radius: the size the locus of local otsu should have
    :return: subplots with match image dice score and colour background depending on in- decrease
    """

    colour = enh.colour_indication(score_increase)

    axes[x].imshow(match_local, cmap=plt.cm.gray)
    axes[x].set_title(f'{radius}\n {round(score_increase, 6)}', fontsize=15, bbox=dict(facecolor=colour, alpha=1.5))
    axes[x].axis('off')


def fig_dif_mask_size(image_directory, control_directory):
    """
    created all parameters for figure with imported subplots
    :param image_directory: directory where the images can be found
    :param control_directory: directory where the controls can be found
    :return: a figure with the thresholds of global and optimal and the matches/scores of different radii
    """

    global_score_list = []

    path_list, name_list = im.image_path_name_list(image_directory, '24h 1_c5.TIF')
    # generates a list of all paths and names of searched images

    figure, axes = plt.subplots(1, 7, figsize=(30, 10))

    for idx, path in enumerate(path_list, 0):

        print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4] + '.*')
        original_image = im.import_image(path)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary_original = original_image > thresh_value
        binary_control, counter = im.assemble_import_control_image(control_directory, control_search_filter)

        match_global = dic.creation_of_match_array(binary_original, binary_control)
        dice_score_global = dic.dice_score(binary_original, binary_control)
        global_score_list.append(dice_score_global)
        # local_score_list.append(dice_score_local)

        axes_otsu_filter_masks(axes, binary_original, binary_control, match_global,
                               dice_score_global)

        radius_list = np.array([0.28, 0.282, 0.285, 5])
        for dx, radius in enumerate(radius_list, 3):
            # local_otsu = enh.local_otsu(original_image, radius)

            gauss_filtered_image = enh.gaussian_filter(original_image, radius)
            gauss_thresh_value = skimage.filters.threshold_otsu(gauss_filtered_image)

            binary_gauss = gauss_filtered_image > gauss_thresh_value
            match_gauss = dic.creation_of_match_array(binary_gauss, binary_control)
            dice_score_gauss = dic.dice_score(binary_gauss, binary_control)

            score_increase = dice_score_gauss - dice_score_global
            x_axis_masks(axes, dx, match_gauss, score_increase, radius)

    plt.show()
    total_dice_score = (sum(global_score_list))/len(path_list)
    print('Total dice score: ', total_dice_score)


def display_improve_gaussian_filter():

    control = 'BBBC020_v1_outlines_nuclei.zip'
    testing = 'BBBC020_v1_images.zip'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = 'all images/BBBC020_v1_images/'
    control_directory = 'all controls/BBC020_v1_outlines_nuclei/'

    # fig_dif_mask_size(image_directory, control_directory)
    radius_list = np.array([0.28, 0.3, 0.5, 1, 2, 3, 4, 5, 7])

    # global_score_list = []
    global_mean_score_list = []

    path_list, name_list = im.image_path_name_list(image_directory, '_c5.TIF')
    # generates a list of all paths and names of searched images

    for dx, radius in enumerate(radius_list):
        current_score_list = []
        # print(radius)
        for idx, path in enumerate(path_list):

            # print(idx, name_list[idx])

            control_search_filter = re.compile(name_list[idx][:-4] + '.*')
            original_image = im.import_image(path)
            binary_control, counter = im.assemble_import_control_image(control_directory, control_search_filter)

            # local_otsu = loco.local_otsu(original_image, radius)
            gauss_filtered_image = enh.gaussian_filter(original_image, radius)
            gauss_thresh_value = skimage.filters.threshold_otsu(gauss_filtered_image)
            binary_gauss = gauss_filtered_image > gauss_thresh_value

            dice_score_global = dic.dice_score(binary_gauss, binary_control)

            current_score_list.append(dice_score_global)

        global_mean_score_list.append(sum(current_score_list)/len(current_score_list))

    # print(global_mean_score_list)

    # radius_list = np.array([1, 2, 3])
    # global_mean_score_list = np.array([0.9, 0.99, 0.98])
    plt.plot(radius_list, global_mean_score_list, 'g-', linewidth=2)
    global_otsu_mean = 0.9847390203373723
    plt.axhline(y=global_otsu_mean, color='r', linestyle='--', linewidth=1, label='Average Dice Score')
    plt.legend()
    plt.title('Sigma Dependent Dice Score')
    plt.xlabel('Sigma')
    plt.ylabel('Dice Score')
    plt.show()


def display_improve_median_filter():

    control = 'BBBC020_v1_outlines_nuclei.zip'
    testing = 'BBBC020_v1_images.zip'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = 'all images/BBBC020_v1_images/'
    control_directory = 'all controls/BBC020_v1_outlines_nuclei/'

    path_list, name_list = im.image_path_name_list(image_directory, '_c5.TIF')
    # generates a list of all paths and names of searched images

    for idx, path in enumerate(path_list):
        # print(idx, name_list[idx])
        control_search_filter = re.compile(name_list[idx][:-4] + '.*')
        original_image = im.import_image(path)
        t = type(original_image)
        print(original_image)
        print(t)
        binary_control, counter = im.assemble_import_control_image(control_directory, control_search_filter)

        # local_otsu = loco.local_otsu(original_image, radius)
        median_filtered_image = enh.median_filter(original_image)
        median_thresh_value = skimage.filters.threshold_otsu(median_filtered_image)
        binary_median = median_filtered_image > median_thresh_value

        dice_score_global_median = dic.dice_score(binary_median, binary_control)

    print('Dice score after median filtering', dice_score_global_median)
    global_otsu_mean = 0.9847390203373723
    print('Dice score increase: ', dice_score_global_median-global_otsu_mean)


# if __name__ == '__main__':
    display_improve_median_filter()


# local otsu


def axes_local_otsus(axes, binary_original, control_image, match_global, dice_score_global):
    """
    A figure is created and shown with 6 subplots for y images
    :param axes: axes for a figure defined in main
    :param binary_original: the optimal value of the threshold is added
    :param control_image: the assembled given control is placed
    :param match_global: the deviation overlay is placed
    :param dice_score_global: a number representing the dice score is inserted
    :return: six subplots original, histogram, thresholded, optimal, matches and dice score without a figure
    """

    axes[0][0].imshow(binary_original, cmap=plt.cm.gray)
    axes[0][0].set_title('Global Otsu')
    axes[0][0].axis('off')

    axes[0][1].imshow(control_image, cmap=plt.cm.gray)
    axes[0][1].set_title('Optimal threshold')
    axes[0][1].axis('off')

    axes[0][2].imshow(match_global, cmap=plt.cm.gray)
    axes[0][2].set_title(f'deviation of global\n {dice_score_global}')
    axes[0][2].axis('off')


def x_axis_local(axes, x, match_local, score_increase, radius, otsu_mask):
    """

    :param axes: axes for a figure defined in main
    :param x: horizontal position of axes in figure
    :param match_local: the deviation overlay between control images and local thresholded is placed
    :param score_increase: local - global otsu
    :param radius: the size the locus of local otsu should have
    :param otsu_mask: showing the map of threshold values
    :return: subplots with match image dice score and colour background depending on in- decrease
    """

    colour = enh.colour_indication(score_increase)

    axes[0][x].imshow(match_local, cmap=plt.cm.gray)
    axes[0][x].set_title(f'{radius}\n {round(score_increase, 6)}', fontsize=15, bbox=dict(facecolor=colour, alpha=1.5))
    axes[0][x].axis('off')

    axes[1][x].imshow(otsu_mask, cmap=plt.cm.gray)


def fig_diff_local_size(image_directory, control_directory):
    """
    created all parameters for figure with imported subplots
    :param image_directory: directory where the images can be found
    :param control_directory: directory where the controls can be found
    :return: a figure with the thresholds of global and optimal and the matches/scores of different radii
    """

    global_score_list = []
    # local_score_list = []

    path_list, name_list = im.image_path_name_list(image_directory, '24h 1_c5.TIF')
    # generates a list of all paths and names of searched images

    figure, axes = plt.subplots(2, 7, figsize=(30, 10))

    for idx, path in enumerate(path_list, 0):

        print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4] + '.*')
        original_image = im.import_image(path)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary_original = original_image > thresh_value
        binary_control, counter = im.assemble_import_control_image(control_directory, control_search_filter)

        match_global = dic.creation_of_match_array(binary_original, binary_control)
        dice_score_global = dic.dice_score(binary_original, binary_control)
        global_score_list.append(dice_score_global)
        # local_score_list.append(dice_score_local)

        axes_local_otsus(axes, binary_original, binary_control, match_global,
                         dice_score_global)

        radius_list = [45, 86, 120]
        for dx, radius in enumerate(radius_list, 3):
            local_otsu, otsu_mask = enh.local_otsu(original_image, radius)
            match_local = dic.creation_of_match_array(local_otsu, binary_control)
            dice_score_local = dic.dice_score(local_otsu, binary_control)
            score_increase = dice_score_local - dice_score_global
            x_axis_local(axes, dx, match_local, score_increase, radius, otsu_mask)

    plt.show()
    # total_dice_score = (sum(global_score_list))/len(path_list)
    # print('Total dice score: ', total_dice_score)


def optimal_local_otsu():

    control = 'BBBC020_v1_outlines_nuclei.zip'
    testing = 'BBBC020_v1_images.zip'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = 'all images/BBBC020_v1_images/'
    control_directory = 'all controls/BBC020_v1_outlines_nuclei/'

    # fig_diff_local_size(image_directory, control_directory)
    radius_list = np.concatenate((10, 25, np.arange(30, 55, 5), 60, 75, 100, 120, 150, 200, 300, 400, 600, 1000),
                                 axis=None)
    # radius_list = np.arange(150, 320, 20)

    # global_score_list = []
    local_mean_score_list = []

    path_list, name_list = im.image_path_name_list(image_directory, '_c5.TIF')
    # generates a list of all paths and names of searched images

    for dx, radius in enumerate(radius_list, 0):
        current_score_list = []
        # print(radius)
        for idx, path in enumerate(path_list, 0):

            # print(idx, name_list[idx])

            control_search_filter = re.compile(name_list[idx][:-4] + '.*')
            original_image = im.import_image(path)
            binary_control, counter = im.assemble_import_control_image(control_directory, control_search_filter)

            local_otsu, otsu_mask = enh.local_otsu(original_image, radius)
            dice_score_local = dic.dice_score(local_otsu, binary_control)

            current_score_list.append(dice_score_local)

        local_mean_score_list.append(sum(current_score_list)/len(current_score_list))

    # print(local_mean_score_list)

    # radius_list = np.array([1, 2, 3])
    # local_mean_score_list = np.array([0.9, 0.99, 0.98])
    plt.plot(radius_list, local_mean_score_list, 'g-', linewidth=2)
    global_otsu_mean = 0.9847390203373723
    plt.axhline(y=global_otsu_mean, color='r', linestyle='--', linewidth=1, label='Average Dice Score')
    plt.legend()
    plt.title('Radius Dependent Dice Score')
    plt.xlabel('Loci Radius')
    plt.ylabel('Dice Score')
    plt.show()


if __name__ == '__main__':
    optimal_local_otsu()
