import numpy as np
import cv2
from os import walk
import sys

row = int(sys.argv[1])
col = int(sys.argv[2])

_, _, filenames = next(walk("results_alldir/"))

for result in sorted(filenames):
    img = cv2.imread('results_alldir/' + result)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    noisySignal = np.asarray(img)
    print(result + "[{}][{}]".format(sys.argv[1], sys.argv[2]))
    print(noisySignal[row][col])




