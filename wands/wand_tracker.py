import cv2

class Tracker:
    def __init__(self) -> None:
        pass

    def add_frame(self, frame):
        single = frame[:,:,1]
        # convert the grayscale image to binary image
        ret,thresh = cv2.threshold(single,225,255,0)

        # calculate moments of binary image
        M = cv2.moments(thresh)
        
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)
