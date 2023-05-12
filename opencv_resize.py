import cv2

# Load the image
img = cv2.imread('C:/Users/drago/Downloads/test2.jpg')

# Resize the image to a new width and height
new_width = 1920    
new_height = 1920
resized_img = cv2.resize(img, (new_width, new_height))

# Display the original and resized images
cv2.imshow('Original Image', img)
cv2.imshow('Resized Image', resized_img)
cv2.waitKey(2)

cv2.imwrite("C:/Users/drago/Downloads/testR2.jpg",resized_img)
cv2.destroyAllWindows()
