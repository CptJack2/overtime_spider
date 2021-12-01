import cv2
import numpy as np

# read input image
img = cv2.imread('a.png')

# define border color
lower = (198,201,204)
upper = (230,232,235)

# convert img to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# threshold on border color
mask = cv2.inRange(gray, 200, 255)

mask=255-mask

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
#mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
# mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
# mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)


# find contours and bounding boxes
bboxes = []
bboxes_img = img.copy()

contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
for cntr in contours:
    x,y,w,h = cv2.boundingRect(cntr)
    cv2.rectangle(bboxes_img, (x, y), (x+w, y+h), (0, 0, 255), 1)
    bboxes.append((x,y,w,h))

# get largest width of bboxes
maxwidth = max(bboxes)[2]

# sort bboxes on x coordinate
def takeFirst(elem):
    return elem[0]

bboxes.sort(key=takeFirst)

# stack cropped boxes with 10 pixels padding all around
result = np.full((1,maxwidth+20,3), (255,255,255), dtype=np.uint8)
for bbox in bboxes:
    (x,y,w,h) = bbox
    crop = img[y-10:y+h+10, x-10:x+maxwidth+10]
    result = np.vstack((result, crop))

# save result
cv2.imwrite("abcd_test_mask.jpg", mask)
cv2.imwrite("abcd_test_white_border.jpg", img)
cv2.imwrite("abcd_test_thresh.jpg", thresh)
cv2.imwrite("abcd_test_morph.jpg", morph)
cv2.imwrite("abcd_test_bboxes.jpg", bboxes_img)
cv2.imwrite("abcd_test_column_stack.png", result)

# show images
cv2.imshow("mask", mask)
cv2.imshow("img", img)
cv2.imshow("thresh", thresh)
cv2.imshow("morph", morph)
cv2.imshow("bboxes_img", bboxes_img)
cv2.imshow("result", result)
cv2.waitKey(0)