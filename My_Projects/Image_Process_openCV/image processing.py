from __future__ import print_function
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import cv2
import imageio
from skimage import io, filters
from scipy import ndimage
import matplotlib.pyplot as plt
from skimage import measure


def dominantColour(image):
    NUM_CLUSTERS = 5

    ##print('reading image')
    im = Image.open(image)
    im = im.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

    ##print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
##    print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = np.histogram(vecs, len(codes))    # count occurrences

    index_max = np.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    print("Ram.....")
##    print(len(peak))
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    print('Most dominant colour is : #%s' % (colour))

    c = ar.copy()
    for i, code in enumerate(codes):
        c[np.r_[np.where(vecs==i)],:] = code
    imageio.imwrite('out.png', c.reshape(*shape).astype(np.uint8))
    print('image saved')


def countObjects(image):
    im = cv2.imread(image, 0)
    plt.imshow(im)
    plt.show()
    val = filters.threshold_otsu(image = im)
    print("Number of chocolates : "+str(val))
    drops = ndimage.binary_fill_holes(im < val)
    plt.imshow(drops)
    plt.show()

    labels = measure.label(drops)
##    print(labels.max())

if __name__ == '__main__':
    dominantColour("image.png")
    countObjects("out.png")
    
