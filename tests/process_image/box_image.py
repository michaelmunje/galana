import os
import cv2
import numpy as np

image_path = os.getcwd() + '/252342.jpg'

# Minimum percentage of pixels of same hue to consider dominant colour
MIN_PIXEL_CNT_PCT = (1.0/20.0)

image = cv2.imread(image_path)
if image is None:
    print("Failed to load iamge.")
    exit(-1)

image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
h,_,_ = cv2.split(image_hsv)

bins = np.bincount(h.flatten())
# And then find the dominant hues
peaks = np.where(bins > (h.size * MIN_PIXEL_CNT_PCT))[0]

print(peaks)
# exit(0)

# Now let's find the shape matching each dominant hue
for i, peak in enumerate(peaks):
    peak = np.array(peak, dtype='uint8')
    # First we create a mask selecting all the pixels of this hue
    mask = cv2.inRange(h, peak, peak)
    # And use it to extract the corresponding part of the original colour image
    blob = cv2.bitwise_and(image, image, mask=mask)

    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for j, contour in enumerate(contours):
        bbox = cv2.boundingRect(contour)
        # Create a mask for this contour
        contour_mask = np.zeros_like(mask)
        cv2.drawContours(contour_mask, contours, j, 255, -1)

        # print("Found hue %d in region %s." % (peak, bbox))
        # Extract and save the area of the contour
        # region = blob.copy()[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2]]
        # region_mask = contour_mask[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2]]
        # region_masked = cv2.bitwise_and(region, region, mask=region_mask)
        # file_name_section = os.getcwd() + "/bbox/colourblobs-%d-hue_%03d-region_%d-section.jpg" % (i, peak, j)
        # cv2.imwrite(file_name_section, region_masked)
        # print(" * wrote '%s'" % file_name_section)

        # Extract the pixels belonging to this contour
        result = cv2.bitwise_and(blob, blob, mask=contour_mask)
        # And draw a bounding box
        top_left, bottom_right = (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3])
        cv2.rectangle(result, top_left, bottom_right, (255, 255, 255), 2)
        file_name_bbox = os.getcwd() + "/bbox/colourblobs-%d-hue_%03d-region_%d-bbox.jpg" % (i, peak, j)
        cv2.imwrite(file_name_bbox, result)
        print(" * wrote '%s'" % file_name_bbox)