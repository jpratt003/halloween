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

import wand_tracker

def _play_video_file(video_filename, tracker):
    print(f"Opening video {video_filename}")
    cap = cv2.VideoCapture(video_filename)
    frame_count = 0
    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            cX,cY = tracker.add_frame(frame)
            if frame_count == tracker.HISTORY_DEPTH:
                angle = tracker.get_wand_angle()
                print(f"Current Angle {angle}")
                frame_count = 0
            frame_count += 1

            cv2.circle(frame, (cX, cY), 15, (255, 255, 255), -1)
            # Display the resulting frame
            cv2.imshow('Frame',frame)
        
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