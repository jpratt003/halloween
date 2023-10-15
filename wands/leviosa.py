__copyright__ = """

    Copyright 2023 John Pratt

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from switched_outlet import SwitchedOutlet
from spell import Spell

if __name__ == "__main__":
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    outlet = SwitchedOutlet()

    def _spell_success():
        print("Leviosa!")
        outlet.toggle(4.)

    leviosa = Spell(["right", "down"], _spell_success)
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # allow the camera to warmup
    time.sleep(0.1)
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        cX,cY = leviosa.add_frame(image)

        cv2.circle(image, (cX, cY), 15, (255, 255, 255), -1)
        oldest_center, newest_center = leviosa._wand_tracker._get_wand_history()
        cv2.line(frame, oldest_center, newest_center, (255,0,0), 5)
        # Display the resulting frame
        cv2.imshow('Frame',image)

        deltaX, deltaY = leviosa._wand_tracker._get_dx_dy()
        line_start = (int(100 - deltaX/2), int(100 - deltaY/2))
        line_end = (int(100 + deltaX/2), int(100 + deltaY/2))
        compass_img = np.zeros((200, 200, 3), np.uint8)
        cv2.line(compass_img, line_start, line_end, (255, 0, 0), 5)

        movement_name = leviosa._wand_tracker.get_movement_name()
        cv2.putText(compass_img, movement_name, (50,50), cv2.FONT_HERSHEY_SIMPLEX,  
                        1, (255,0,0), 2, cv2.LINE_AA) 

        cv2.imshow("Compass", compass_img)
    
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break