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
import enhance as enh
from skimage.color import label2rgb
from scipy import ndimage as ndi
import re


def axes_original_hist_otsus(axes, y, original_image, binary_original, thresh_value, control_image,
                             name, local_threshold, match_global, match_local, dice_score_global,
                             dice_score_local, score_increase, radius, global_count, local_count, op_count):

    """
    A figure is created and shown with 6 subplots for y images
    :param axes:  axes for a figure defined in main
    :param y:  vertical position of axes in figure
    :param original_image: untreated image is placed
    :param binary_original: the optimal value of the threshold is added
    :param thresh_value: image after otsu thresholding is placed
    :param control_image: the assembled given control is placed
    :param name: the name of the searched image
    :param local_threshold: an array with each pixel's threschold
    :param match_global: the deviation overlay of global otsu and optimum is placed
    :param match_local: the deviation overlay local otsu and optimum is placed
    :param dice_score_global: a number representing the dice score is inserted
    :param dice_score_local: dice score of the local otsu approach
    :param score_increase: local - global otsu
    :param radius: the size the locus of local otsu should have
    :param global_count: nuclei counts after global otsu
    :param local_count: nuclei counts after local otsu
    :param op_count: nuclei counts of given optimum
    :return: six subplots original, histogram, global-thresholded, local-thresholded, optimal,
             matches of local and global and dice score without a figure
    """

    axes[y][1].imshow(original_image, cmap=plt.cm.gray)
    axes[y][1].set_title('Original: ' + name)
    axes[y][1].axis('off')

    axes[y][0].hist(original_image.ravel(), bins=256)
    axes[y][0].set_ylim(top=20000)
    axes[y][0].set_title('Intensity Histogram')
    axes[y][0].axvline(thresh_value, color='r', label='Threshold Value')
    axes[y][0].legend()

    axes[y][2].imshow(binary_original, cmap=plt.cm.gray)
    axes[y][2].set_title('Global Otsu')
    axes[y][2].axis('off')

    axes[y][3].imshow(local_threshold, cmap=plt.cm.gray)
    axes[y][3].set_title(f'Local thresholding {radius}\n segmented')
    axes[y][3].axis('off')

    axes[y][4].imshow(control_image, cmap=plt.cm.gray)
    axes[y][4].set_title('Ground Truth')
    axes[y][4].axis('off')

    axes[y][5].imshow(match_global, cmap=plt.cm.gray)
    axes[y][5].set_title(f'Deviation with Global\n {round(dice_score_global, 6)}')
    axes[y][5].axis('off')

    axes[y][6].imshow(match_local, cmap=plt.cm.gray)
    axes[y][6].set_title(f'Deviation with Local\n {round(dice_score_local, 6)}')
    axes[y][6].axis('off')

    colour = enh.colour_indication(score_increase)

    axes[y][7].text(0, 1, f'Increase by Local Otsu, Object Deletion :\n {round(score_increase, 6)}', fontsize=15,
                    bbox=dict(facecolor=colour, alpha=1.5))
    axes[y][7].text(0, 0.2, f'Nuclei number\n Global: {global_count}\n Local: {local_count}\n Optimal: {op_count}',
                    fontsize=15)
    axes[y][7].axis('off')


def main():

    control = 'BBBC020_v1_outlines_nuclei.zip'
    testing = 'BBBC020_v1_images.zip'
    im.create_unzipped_files_if_there_are_no(control, 'all controls')
    im.create_unzipped_files_if_there_are_no(testing, 'all images')
    image_directory = 'all images/BBBC020_v1_images/'
    control_directory = 'all controls/BBC020_v1_outlines_nuclei/'

    global_score_list = []
    local_score_list = []

    path_list, name_list = im.image_path_name_list(image_directory, '_c5.TIF')
    # generates a list of all paths and names of searched images

    figure, axes = plt.subplots(20, 8, figsize=(25, 50))

    for idx, path in enumerate(path_list, 0):
        # print(idx, name_list[idx])

        control_search_filter = re.compile(name_list[idx][:-4]+'.*')
        original_image = im.import_image(path)
        # original_image = sk.img_as_ubyte(original_image)
        thresh_value = skimage.filters.threshold_otsu(original_image)
        # image is binarized(False = black, True = white) and final figure is created
        binary_original = original_image > thresh_value
        binary_control, optimal_counter = im.assemble_import_control_image(control_directory, control_search_filter)

        # print('opimal nuclei:', optimal_counter)

        radius = 45
        original_image_filtered = enh.median_filter(original_image)
        local_otsu, mask = enh.local_otsu(original_image_filtered, radius)

        cleaned_original = enh.small_obj_deletion(binary_original, 900)  # small objects were erased
        g_segmented, global_count = ndi.label(cleaned_original)  # nuclei were marked and counted
        match_global = dic.creation_of_match_array(binary_original, binary_control)
        # print('global nuclei: ', global_count)

        local_otsu = enh.small_obj_deletion(local_otsu, 900)  # small objects were erased
        l_segmented, local_count = ndi.label(local_otsu)  # nuclei were marked and counted
        match_local = dic.creation_of_match_array(local_otsu, binary_control)
        coloured_local = label2rgb(l_segmented, bg_label=0, bg_color=(0, 0, 0))
        # print('local nuclei: ', local_count)

        dice_score_global = dic.dice_score(binary_original, binary_control)
        dice_score_local = dic.dice_score(local_otsu, binary_control)
        global_score_list.append(dice_score_global)
        local_score_list.append(dice_score_local)
        score_increase = dice_score_local-dice_score_global

        axes_original_hist_otsus(axes, idx, original_image, binary_original, thresh_value, binary_control,
                                 name_list[idx], coloured_local, match_global, match_local, dice_score_global,
                                 dice_score_local, score_increase, radius, global_count, local_count, optimal_counter)

    figure.tight_layout()
    figure.show()
    total_dice_score = (sum(global_score_list))/len(global_score_list)
    print('Average GlobalDice score: ', total_dice_score)
    average_local_dice_score = (sum(local_score_list))/len(local_score_list)
    print('Average Local Dice score: ', average_local_dice_score)


if __name__ == '__main__':
    main()
