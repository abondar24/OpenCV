import cv2
import numpy as np
import os

image = cv2.imread('hard.jpg')

cv2.imwrite('president.jpg', image)

gray_image = cv2.imread('hard.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
cv2.imwrite('pr1.png', gray_image)

random_byte_array = bytearray(os.urandom(120000))
flat_numpy_array = np.array(random_byte_array)
gray_image = flat_numpy_array.reshape(300, 400)
cv2.imwrite('random_gray.png', gray_image)

bgr_image = flat_numpy_array.reshape(100, 400, 3)
cv2.imwrite('RandomColor.png', bgr_image)