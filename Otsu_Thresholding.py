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
import enhance as loco
import re
import os


def figure_of_original_histogram_and_otsu(axes, y, original_image, binary_original, thresh_value, control_image,
                                          name, local_threshold, match_global, match_local, dice_score_global,
                                          dice_score_local, score_increase, radius):

    """
    A figure is created and shown with 6 subplots for y images
    :param axes:  axes for a figure defined in main
    :param y:  vertical position of axes in figure
    :param original_image: untreated image is placed
    :param binary_original: the optimal value of the threshold is added
    :param thresh_value: image after otsu thresholding is placed
    :param control_image: the assembled given control is placed
    :param name: the name of the seached image
    :param local_threshold: an array with eache pixel's threschold
    :param match_global: the deviation overlay of global otsu and optimum is placed
    :param match_local: the deviation overlay local otsu and optimum is placed
    :param dice_score_global: a number repesenting the dice score is inserted
    :param dice_score_local: dice score of the local otsu approach
    :param score_increase: local - global otsu
    :param radius: the size the locus of local otsu should have
    :return: six subplots original, histogram, global-thresholded, local-thresholded, optimal,
             matches of local and global and dice score without a figure
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

    axes[y][3].imshow(local_threshold, cmap=plt.cm.gray)
    axes[y][3].set_title(f'local thresholding\n {radius}')
    axes[y][3].axis('off')

    axes[y][4].imshow(control_image, cmap=plt.cm.gray)
    axes[y][4].set_title('Optimal threshold')
    axes[y][4].axis('off')

    axes[y][5].imshow(match_global, cmap=plt.cm.gray)
    axes[y][5].set_title(f'deviation of global\n {dice_score_global}')
    axes[y][5].axis('off')

    axes[y][6].imshow(match_local, cmap=plt.cm.gray)
    axes[y][6].set_title(f'deviation of local\n {dice_score_local}')
    axes[y][6].axis('off')

    if score_increase > 0:
        c = 'green'
    elif score_increase < 0:
        c = "red"
    else:
        c = "yellow"
    axes[y][7].text(0, 0.5, f"Increase: {round(score_increase, 6)}", fontsize=19, bbox=dict(facecolor=c, alpha=1.5))
    axes[y][7].axis('off')


def main():

    control = 'BBBC020_v1_outlines_nuclei.zip'
    testing = 'BBBC020_v1_images.zip'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = "all images/BBBC020_v1_images/"

    image_path_list = []
    name_list = []
    global_score_list = []
    local_score_list = []

    for root, dirs, files in os.walk(image_directory, topdown=False):
        for name in files:
            image_paths = os.path.join(root, name)  # join directory and namr to path

            # image paths fulfilling name_criteria are selected
            name_criteria = "_c5.TIF"
            length = len(name_criteria)
            if image_paths[-length:] == name_criteria:  # if the last (length) digits fulfill name criteria -> move on
                image_path_list.append(image_paths)
                name_list.append(name)

    figure, axes = plt.subplots(20, 8, figsize=(24, 60))

    for idx, path in enumerate(image_path_list, 0):
        print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4]+".*")
        original_image = im.import_image(path)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary_original = original_image > thresh_value
        control_directory = "all controls/BBC020_v1_outlines_nuclei/"
        binary_control = im.assemble_and_import_control_image(control_directory, control_search_filter)

        radius = 1
        local_otsu = loco.local_otsu(original_image, radius)

        match_global = dic.creation_of_match_array(binary_original, binary_control)
        match_local = dic.creation_of_match_array(local_otsu, binary_control)

        dice_score_global = dic.dice_score(binary_original, binary_control)
        dice_score_local = dic.dice_score(local_otsu, binary_control)
        global_score_list.append(dice_score_global)
        local_score_list.append(dice_score_local)
        score_increase = dice_score_local-dice_score_global

        figure_of_original_histogram_and_otsu(axes, idx, original_image, binary_original, thresh_value, binary_control,
                                              name_list[idx], local_otsu, match_global, match_local, dice_score_global,
                                              dice_score_local, score_increase, radius)

    plt.show()
    total_dice_score = (sum(global_score_list))/len(global_score_list)
    print('Total dice score: ', total_dice_score)


if __name__ == "__main__":
    main()
