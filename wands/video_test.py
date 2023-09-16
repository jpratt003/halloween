import argparse
import cv2

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