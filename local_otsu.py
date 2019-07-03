# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:08:50 2019
local otsu
@author: Luis
"""

from skimage import data
from skimage.morphology import disk
from skimage.filters import threshold_otsu, rank
from skimage.util import img_as_ubyte
import skimage as sk
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.size'] = 9
# img = img_as_ubyte(data.page())
img = sk.io.imread('all images/BBBC020_v1_images/jw-1h 1/jw-1h 1_c5.TIF', as_gray=True)
# img = img_as_ubyte('all images/BBBC020_v1_images/jw-1h 1/jw-1h 1_c5.TIF')



radius = 200
selem = disk(radius)

local_otsu = rank.otsu(img, selem)
# sk.io.imsave('test.png', local_otsu)
# local_otsu = sk.io.imread(local_otsus, as_gray=True)

threshold_global_otsu = threshold_otsu(img)
global_otsu = img >= threshold_global_otsu

fig, ax = plt.subplots(2, 2, figsize=(8, 5), sharex=True, sharey=True,
                       subplot_kw={'adjustable': 'box-forced'})
ax0, ax1, ax2, ax3 = ax.ravel()
plt.tight_layout()

fig.colorbar(ax0.imshow(img, cmap=plt.cm.gray),
             ax=ax0, orientation='horizontal')
ax0.set_title('Original')
ax0.axis('off')

h = local_otsu
fig.colorbar(ax1.imshow(local_otsu, cmap=plt.cm.gray),
             ax=ax1, orientation='horizontal')
ax1.set_title('Local Otsu (radius=%d)' % radius)
ax1.axis('off')

ax2.imshow((img+0.01)*87.5 >= local_otsu, cmap=plt.cm.gray)  # TODO unbelievable sketchy get scale done
ax2.set_title('Original >= Local Otsu' % threshold_global_otsu)
ax2.axis('off')

ax3.imshow(global_otsu, cmap=plt.cm.gray)
ax3.set_title('Global Otsu (threshold = %d)' % threshold_global_otsu)
ax3.axis('off')

plt.show()
print(h)
print(img)