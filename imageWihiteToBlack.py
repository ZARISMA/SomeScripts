import cv2

# Load the image
img = cv2.imread('C:\Project1\MYPROJ\photo.jpg', cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur (optional, for noise reduction)
blur = cv2.GaussianBlur(img, (5, 5), 0)

# Apply binary inverse threshold
# This will make the text white and background black
_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Save or display
cv2.imwrite('output.png', binary)
