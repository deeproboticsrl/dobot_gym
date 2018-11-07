import cv2
import numpy as np
import copy
##low :[  0 208  61], high:[ 74 255 153]
##low :[  0 187  71], high:[ 80 245 255]
class Vision():
    def __init__(self):

    # cap1 = cv2.VideoCapture(1)
    cap2 = cv2.VideoCapture(2)

    def get_obs_cam(centroid=True)
    # Capture frame-by-frame
    # ret1, right = cap1.read()
        ret2, left =  cap2.read()

    #  operations on the frame come here
        # hsv_right = cv2.cvtColor(right, cv2.COLOR_BGR2HSV)
        hsv_left = cv2.cvtColor(left, cv2.COLOR_BGR2HSV)

        lower_orange= np.array([0,187,71])
        upper_orange = np.array([80,245,255])

        mask = cv2.inRange(hsv_left, lower_orange, upper_orange)
    # Bitwise-AND mask and original image
        res = cv2.bitwise_and(left, left, mask=mask)
        if centroid:
            kernel = np.ones((3, 3), np.uint8)
            erosion = cv2.erode(mask, kernel, iterations=1)
            M = cv2.moments(erosion)
            cX=-1
            cY=-1
            if M["m00"] !=0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            return left,[cX,cY]
        return left


    def show_image()
        ret2,im = cap2.read()
        while(True):


            cv2.circle(im, (cX, cY), 5, (255, 255, 255), -1)
    # Display the resulting frame
    # cv2.imshow('right', right)
            cv2.imshow('left', im)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# When everything done, release the capture
# cap1.release()
#         cap2.release()
        cv2.destroyAllWindows()