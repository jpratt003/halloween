
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

import wand_tracker
from typing import List, Callable, Tuple
import cv2
class Spell:
    def __init__(self, movements:List[str], callback) -> None:
        self._callback = callback
        self._movements = movements
        self._wand_tracker = wand_tracker.Tracker()
        self._tracking_idx = 0

    def add_frame(self, frame) -> Tuple[int, int]:
        center_point =  self._wand_tracker.add_frame(frame)
        current_movement = self._wand_tracker.get_movement_name()
        if current_movement == self._movements[self._tracking_idx]:
            # We found the next movement, update the tracking index
            if self._tracking_idx == len(self._movements) - 1:
                # Successful end of the spell!
                self._callback()
                self._tracking_idx = 0
            else:
                self._tracking_idx +=1
        elif (self._tracking_idx > 0 and current_movement == self._movements[self._tracking_idx - 1]) or current_movement == "":
            # No need to make any updates, still tracking the same movement or paused in the movement
            pass
        else:
            self._tracking_idx = 0
        return center_point