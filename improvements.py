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

# edging


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

    colour = enh.colour_indication(score_increase)

    axes[7].imshow(match_local, cmap=plt.cm.gray)
    axes[7].set_title(f'{radius}\n {round(score_increase, 6)}', fontsize=15, bbox=dict(facecolor=colour, alpha=1.5))
    axes[7].axis('off')


def figure_of_different_disc_size(image_directory, control_directory):
    """
    created all parameters for figure with imported subplots
    :param image_directory: directory where the images can be found
    :param control_directory: directory where the controls can be found
    :return: a figure with the thresholds of global and optimal and the matches/scores of different radii
    """

    global_score_list = []
    # local_score_list = []

    path_list, name_list = im.image_path_name_list(image_directory, '1h 1_c5.TIF')

    figure, axes = plt.subplots(1, 8, figsize=(30, 10))

    for idx, path in enumerate(path_list, 0):

        print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4] + '.*')
        original_image = im.import_image(path)
        original_image = img_as_ubyte(original_image)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary_original = original_image > thresh_value

        binary_control = im.assemble_import_control_image(control_directory, control_search_filter)

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


def increase_add_edge():

    control = 'BBBC020_v1_outlines_nuclei.zip'
    testing = 'BBBC020_v1_images.zip'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = 'all images/BBBC020_v1_images/'
    control_directory = 'all controls/BBC020_v1_outlines_nuclei/'

    # figure_of_different_disc_size(image_directory, control_directory)

    radius_list = np.array([1])

    # global_score_list = []
    mean_score_after_edging = []

    path_list, name_list = im.image_path_name_list(image_directory, '_c5.TIF')

    for dx, radius in enumerate(radius_list):
        current_score_list = []
        print(radius)
        for idx, path in enumerate(path_list):

            print(idx, name_list[idx])

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

            binary_control = im.assemble_import_control_image(control_directory, control_search_filter)

            dice_score_global = dic.dice_score(binary_sobel, binary_control)

            current_score_list.append(dice_score_global)

        mean_score_after_edging.append(sum(current_score_list)/len(current_score_list))

    print(mean_score_after_edging)

    # radius_list = np.array([1, 2, 3])
    # mean_score_after_edging = np.array([0.9, 0.99, 0.98])
    global_otsu_mean = 0.9847390203373723  # as list for compatibility with mean score afteredging
    score_increase = mean_score_after_edging[0]-global_otsu_mean

    colour = enh.colour_indication(score_increase)

    plt.text(0, 0.5, f'Increase:\n {round(score_increase, 6)}', fontsize=19, bbox=dict(facecolor=colour, alpha=1.5))
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    increase_add_edge()

# filtering


def axes_otsu_match(axes, binary_original, control_image, match_global, dice_score_global):
    """
    A figure is created and shown with 6 subplots for y images
    :param axes: axes for a figure defined in main
    :param y: vertical position of axes in figure
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


def x_axis_plots(axes, x, match_local, score_increase, radius):
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
        binary_control = im.assemble_import_control_image(control_directory, control_search_filter)

        match_global = dic.creation_of_match_array(binary_original, binary_control)
        dice_score_global = dic.dice_score(binary_original, binary_control)
        global_score_list.append(dice_score_global)
        # local_score_list.append(dice_score_local)

        axes_otsu_match(axes, binary_original, binary_control, match_global,
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
            x_axis_plots(axes, dx, match_gauss, score_increase, radius)

    plt.show()
    total_dice_score = (sum(global_score_list))/len(path_list)
    print('Total dice score: ', total_dice_score)


def display_improve_filter():

    control = 'BBBC020_v1_outlines_nuclei.zip'
    testing = 'BBBC020_v1_images.zip'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = 'all images/BBBC020_v1_images/'
    control_directory = 'all controls/BBC020_v1_outlines_nuclei/'

    fig_dif_mask_size(image_directory, control_directory)
    radius_list = np.array([0.25, 0.5, 1, 2, 3, 4, 5, 7, 10])

    # global_score_list = []
    global_mean_score_list = []

    path_list, name_list = im.image_path_name_list(image_directory, '1_c5.TIF')
    # generates a list of all paths and names of searched images

    for dx, radius in enumerate(radius_list):
        current_score_list = []
        print(radius)
        for idx, path in enumerate(path_list):

            print(idx, name_list[idx])

            control_search_filter = re.compile(name_list[idx][:-4] + '.*')
            original_image = im.import_image(path)
            binary_control = im.assemble_import_control_image(control_directory, control_search_filter)

            # local_otsu = loco.local_otsu(original_image, radius)
            gauss_filtered_image = enh.gaussian_filter(original_image, radius)
            gauss_thresh_value = skimage.filters.threshold_otsu(gauss_filtered_image)
            binary_gauss = gauss_filtered_image > gauss_thresh_value

            dice_score_global = dic.dice_score(binary_gauss, binary_control)

            current_score_list.append(dice_score_global)

        global_mean_score_list.append(sum(current_score_list)/len(current_score_list))

    print(global_mean_score_list)

    # radius_list = np.array([1, 2, 3])
    # global_mean_score_list = np.array([0.9, 0.99, 0.98])
    plt.plot(radius_list, global_mean_score_list, 'g-', linewidth=2)
    global_otsu_mean = 0.9847390203373723
    plt.axhline(y=global_otsu_mean, color='r', linestyle='--', linewidth=1, label='Total dice score')
    plt.legend()
    plt.title('sigma dependent dice score')
    plt.xlabel('sigma')
    plt.ylabel('dice score')
    plt.show()


if __name__ == '__main__':
    display_improve_filter()


# local otsu


def axes_hist_otsus(axes, binary_original, control_image, match_global, dice_score_global):
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


def x_axis_plots(axes, x, match_local, score_increase, radius):
    """

    :param axes: axes for a figure defined in main
    :param y: vertical position of axes in figure
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

    figure, axes = plt.subplots(1, 7, figsize=(30, 10))

    for idx, path in enumerate(path_list, 0):

        print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4] + '.*')
        original_image = im.import_image(path)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary_original = original_image > thresh_value
        binary_control = im.assemble_import_control_image(control_directory, control_search_filter)

        match_global = dic.creation_of_match_array(binary_original, binary_control)
        dice_score_global = dic.dice_score(binary_original, binary_control)
        global_score_list.append(dice_score_global)
        # local_score_list.append(dice_score_local)

        axes_hist_otsus(axes, binary_original, binary_control, match_global,
                        dice_score_global)

        radius_list = [5, 20, 50, 200]
        for dx, radius in enumerate(radius_list, 3):
            local_otsu = enh.local_otsu(original_image, radius)
            match_local = dic.creation_of_match_array(local_otsu, binary_control)
            dice_score_local = dic.dice_score(local_otsu, binary_control)
            score_increase = dice_score_local - dice_score_global
            x_axis_plots(axes, dx, match_local, score_increase, radius)

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
    # radius_list = np.concatenate((10, 25, np.arange(30, 65, 5), 75, 100, 150, 300, 900), axis=None)
    radius_list = np.arange(40, 51, 1)

    # global_score_list = []
    local_mean_score_list = []

    path_list, name_list = im.image_path_name_list(image_directory, '_c5.TIF')
    # generates a list of all paths and names of searched images

    for dx, radius in enumerate(radius_list, 0):
        current_score_list = []
        print(radius)
        for idx, path in enumerate(path_list, 0):

            print(idx, name_list[idx])

            control_search_filter = re.compile(name_list[idx][:-4] + '.*')
            original_image = im.import_image(path)
            binary_control = im.assemble_import_control_image(control_directory, control_search_filter)

            local_otsu = enh.local_otsu(original_image, radius)
            dice_score_local = dic.dice_score(local_otsu, binary_control)

            current_score_list.append(dice_score_local)

        local_mean_score_list.append(sum(current_score_list)/len(current_score_list))

    print(local_mean_score_list)

    # radius_list = np.array([1, 2, 3])
    # local_mean_score_list = np.array([0.9, 0.99, 0.98])
    plt.plot(radius_list, local_mean_score_list, 'g-', linewidth=2)
    global_otsu_mean = 0.9847390203373723
    plt.axhline(y=global_otsu_mean, color='r', linestyle='--', linewidth=1, label='Total dice score')
    plt.legend()
    plt.title('radius dependent dice score')
    plt.xlabel('disc radius')
    plt.ylabel('dice score')
    plt.show()


if __name__ == '__main__':
    optimal_local_otsu()
