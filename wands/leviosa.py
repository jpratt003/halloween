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

import time
import cv2
import numpy as np
from switched_outlet import SwitchedOutlet
from spell import Spell
from picamera2 import Picamera2

if __name__ == "__main__":
    # initialize the camera and grab a reference to the raw camera capture
    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
    camera.start()
    outlet = SwitchedOutlet()

    def _spell_success():
        print("Leviosa!")
        outlet.toggle(6.)

    leviosa = Spell(["right", "down"], _spell_success)
    # allow the camera to warmup
    time.sleep(0.1)
    # capture frames from the camera
    while True:
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = camera.capture_array()
        image = cv2.flip(image, 0)
        cX,cY = leviosa.add_frame(image)

        if cX is not None and cY is not None:
            cv2.circle(image, (cX, cY), 15, (255, 255, 255), -1)
        oldest_center, newest_center = leviosa._wand_tracker._get_wand_history()
        if oldest_center != (None, None) and newest_center != (None, None):
            cv2.line(image, oldest_center, newest_center, (255,0,0), 5)
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
