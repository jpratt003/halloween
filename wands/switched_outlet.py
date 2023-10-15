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

from gpiozero import LED
import time


class SwitchedOutlet:
    ON_GPIO = 26
    OFF_GPIO = 19

    def __init__(self) -> None:
        # Create both controls and set to 'High'
        # Since that is 'no input'
        self._on_led = LED(self.ON_GPIO)
        self._on_led.on()
        self._off_led = LED(self.OFF_GPIO)
        self._off_led.on()

    def turn_on(self) -> None:
        # Toggle to 'Low' to simulate button press
        self._on_led.off()
        time.sleep(0.2)
        self._on_led.on()

    def turn_off(self) -> None:
        # Toggle to 'Low' to simulate button press
        self._off_led.off()
        time.sleep(0.2)
        self._off_led.on()
