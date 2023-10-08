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

import cv2
import math
from typing import List, Tuple

class Tracker:
    IMAGE_THRESHOLD = 225
    HISTORY_DEPTH = 15
    MIN_MOVEMENT = 100

    def __init__(self) -> None:
        self._center_list = [None for i in range(self.HISTORY_DEPTH)]
        self._center_idx = 0

    def _unwrap_history(self) -> List:
        return [self._center_list[(self._center_idx + idx) % self.HISTORY_DEPTH] for idx in range(self.HISTORY_DEPTH)]

    def add_frame(self, frame):
        single = frame[:,:,1]
        # convert the grayscale image to binary image
        _,thresh = cv2.threshold(single,self.IMAGE_THRESHOLD,255,0)

        # calculate moments of binary image
        M = cv2.moments(thresh)
        
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if self._center_list[self._center_idx] is None:
            self._center_list = [(cX, cY) for i in range(self.HISTORY_DEPTH)]
        else:
            self._center_list[self._center_idx] = (cX, cY)
        self._center_idx = (self._center_idx + 1) % self.HISTORY_DEPTH
        return (cX, cY)

    def get_dx_dy(self) -> Tuple[float, float]:
        startX, startY = self._center_list[self._center_idx - 1]
        endX, endY = self._center_list[self._center_idx]
        deltaX = endX - startX
        deltaY = endY - startY
        return deltaX, deltaY

    def get_wand_movement(self) -> float:
        deltaX, deltaY = self.get_dx_dy()
        radians = math.atan2(deltaY, deltaX)
        degrees = math.degrees(radians)
        dist = math.sqrt(deltaX**2 + deltaY**2)
        return dist, degrees

    def get_wand_history(self) ->Tuple[float, float]:
        return (self._center_list[self._center_idx-1], self._center_list[self._center_idx])

    def get_movement_name(self) -> str:
        dist, degrees = self.get_wand_movement()
        if dist < self.MIN_MOVEMENT:
            return ""
        
        if degrees < 45. and degrees > -.45:
            return "left"
        if degrees > 45. and degrees < 135.:
            return "up"
        if degrees > -135. and degrees < -45.:
            return "down"
        return "right"