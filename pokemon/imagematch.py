import cv2
import numpy as np


template= cv2.imread('sewaddle.jpg')
path="./pokedex_files/540.png"
i=1
image= cv2.imread(path)
result= cv2.matchTemplate(template, image, cv2.TM_CCOEFF)


mn,_,mnLoc,_ = cv2.minMaxLoc(result)

# Draw the rectangle:
# Extract the coordinates of our best match
MPx,MPy = mnLoc

# Step 2: Get the size of the template. This is the same size as the match.
trows,tcols = template.shape[:2]

# Step 3: Draw the rectangle on large_image
cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

cv2.imshow('Rainforest', template)
cv2.waitKey(0)
cv2.destroyAllWindows()
