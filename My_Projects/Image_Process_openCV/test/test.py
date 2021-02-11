import cv2

img = cv2.imread('goku.jpg')
# cv2.imshow('Output', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# resize ?
print("Image dimensions", img.shape)
mySize = (600, 300)
resizeImage = cv2.resize(img, mySize)
cv2.imshow('Output', resizeImage)
cv2.waitKey(0)
cv2.destroyAllWindows()

# -------------------------- Morphology Operations --------------------------------#