import cv2
import numpy as np

img1 = np.zeros((300, 300), np.uint8)
img2 = np.zeros((300, 300), np.uint8)

img1 = cv2.rectangle(img1, (50, 50), (250, 250), 255, -1)

img2 = cv2.circle(img2, (150, 150), 100, 255, -1)

bit_and = cv2.bitwise_and(img1, img2)
bit_or  = cv2.bitwise_or(img1, img2)
bit_xor = cv2.bitwise_xor(img1, img2)
bit_not = cv2.bitwise_not(img1)

cv2.imshow("Image 1", img1)
cv2.imshow("Image 2", img2)
cv2.imshow("Bitwise AND", bit_and)
cv2.imshow("Bitwise OR", bit_or)
cv2.imshow("Bitwise XOR", bit_xor)
cv2.imshow("Bitwise NOT (of Image 1)", bit_not)

cv2.waitKey(0)
cv2.destroyAllWindows()
