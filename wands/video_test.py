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

import argparse
import cv2
import numpy as np

import wand_tracker

def _play_video_file(video_filename, tracker):
    print(f"Opening video {video_filename}")
    cap = cv2.VideoCapture(video_filename)
    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            cX,cY = tracker.add_frame(frame)

            cv2.circle(frame, (cX, cY), 15, (255, 255, 255), -1)
            oldest_center, newest_center = tracker.get_wand_history()
            cv2.line(frame, oldest_center, newest_center, (255,0,0), 5)
            # Display the resulting frame
            cv2.imshow('Frame',frame)

            deltaX, deltaY = tracker.get_dx_dy()
            line_start = (int(100 - deltaX/2), int(100 - deltaY/2))
            line_end = (int(100 + deltaX/2), int(100 + deltaY/2))
            compass_img = np.zeros((200, 200, 3), np.uint8)
            cv2.line(compass_img, line_start, line_end, (255, 0, 0), 5)

            movement_name = tracker.get_movement_name()
            image = cv2.putText(compass_img, movement_name, (50,50), cv2.FONT_HERSHEY_SIMPLEX,  
                            1, (255,0,0), 2, cv2.LINE_AA) 

            cv2.imshow("Compass", compass_img)
        
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        # Break the loop
        else: 
            break

    # When everything done, release the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="input processing file",
                    type=str)
    args = parser.parse_args()
    wand_tracker = wand_tracker.Tracker()
    _play_video_file(args.input, wand_tracker)