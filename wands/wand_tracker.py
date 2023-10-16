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
        self._center_list = [(None,None) for i in range(self.HISTORY_DEPTH)]
        self._center_idx = 0

    def _unwrap_history(self) -> List:
        return [self._center_list[(self._center_idx + idx) % self.HISTORY_DEPTH] for idx in range(self.HISTORY_DEPTH)]

    def _get_dx_dy(self) -> Tuple[float, float]:
        (startX, startY), (endX, endY) = self._get_wand_history()
        if startX is None or startY is None or endX is None or endY is None:
            return 0., 0.
        deltaX = endX - startX
        deltaY = endY - startY
        return deltaX, deltaY

    def _get_wand_movement(self) -> float:
        deltaX, deltaY = self._get_dx_dy()
        radians = math.atan2(deltaY, deltaX)
        degrees = math.degrees(radians)
        dist = math.sqrt(deltaX**2 + deltaY**2)
        return dist, degrees

    def _get_wand_history(self) ->Tuple[float, float]:
        unwrapped_history = self._unwrap_history()
        oldest_idx = 0
        oldest_cx, oldest_cy = unwrapped_history[oldest_idx]
        while oldest_cx is None and oldest_cy is None and oldest_idx < self.HISTORY_DEPTH - 1:
            oldest_idx += 1
            oldest_cx, oldest_cy = unwrapped_history[oldest_idx]

        if oldest_cx is None or oldest_cy is None:
            return (None, None), (None, None)
        newest_idx = self.HISTORY_DEPTH - 1
        newest_cx, newest_cy = unwrapped_history[newest_idx]
        while newest_cx is None and newest_cy is None and newest_idx > 0:
            newest_idx -= 1
            newest_cx, newest_cy = unwrapped_history[newest_idx]

        if newest_cx is None or newest_cy is None:
            return (None, None), (None, None)
        return (oldest_cx, oldest_cy), (newest_cx, newest_cy)

    def clear(self) -> None:
        self._center_list = [(None,None) for i in range(self.HISTORY_DEPTH)]
        self._center_idx = 0

    def add_frame(self, frame):
        single = frame[:,:,1]
        # convert the grayscale image to binary image
        _,thresh = cv2.threshold(single,self.IMAGE_THRESHOLD,255,0)

        # calculate moments of binary image
        M = cv2.moments(thresh)
        
        # calculate x,y coordinate of center
        moments_keys = ["m10", "m00", "m01"]
        if all([moment_key in M for moment_key in moments_keys]) and all([M[moment_key] > 0 for moment_key in moments_keys]):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX = None
            cY = None
        self._center_list[self._center_idx] = (cX, cY)
        self._center_idx = (self._center_idx + 1) % self.HISTORY_DEPTH
        return (cX, cY)

    def get_movement_name(self) -> str:
        dist, degrees = self._get_wand_movement()
        if dist < self.MIN_MOVEMENT:
            return ""
        
        if degrees < 45. and degrees > -.45:
            return "left"
        if degrees > 45. and degrees < 135.:
            return "up"
        if degrees > -135. and degrees < -45.:
            return "down"
        return "right"