import cv2
import numpy as np


# low :[  0 208  61], high:[ 74 255 153]
# low :[  0 187  71], high:[ 80 245 255]
class Vision:
    def __init__(self, camera_port_left=1):
        self.camera_port = camera_port_left
        # self.cap1 = cv2.VideoCapture(2)
        self.cap2 = cv2.VideoCapture(camera_port_left)

    def get_obs_cam(self, centroid=True):
        # Capture frame-by-frame
        # ret1, right = self.cap1.read()
        ret2, left = self.cap2.read()

        #  operations on the frame come here
        # hsv_right = cv2.cvtColor(right, cv2.COLOR_BGR2HSV)
        hsv_left = cv2.cvtColor(left, cv2.COLOR_BGR2HSV)

        lower_orange = np.array([0, 187, 71])
        upper_orange = np.array([80, 245, 255])

        mask = cv2.inRange(hsv_left, lower_orange, upper_orange)
        # Bitwise-AND mask and original image
        #     res = cv2.bitwise_and(left, left, mask=mask)
        if centroid:
            kernel = np.ones((3, 3), np.uint8)
            erosion = cv2.erode(mask, kernel, iterations=1)
            M = cv2.moments(erosion)
            global cX
            global cY
            cX = cY = -1
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            return left, [cX, cY]
        return left

    def show_image(self, render_time=10):

        # ret2,left = self.cap2.read()
        for i in range(render_time):
            left, arr = self.get_obs_cam(centroid=True)
            cv2.circle(left, (arr[0], arr[1]), 5, (255, 255, 255), -1)
            # Display the resulting frame
            print(arr)
            # cv2.imshow('right', right)
            cv2.imshow('left', left)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        # cap1.release()
        #         cap2.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    a = Vision()
    a.show_image(render_time=50000)

# Y axis of the frame :Top to bottom increasing
# X axis of the frame: left to right increasing
