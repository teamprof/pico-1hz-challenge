# Copyright 2025 teamprof.net@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import gc9a01 as gc9a01 

from util import Util
from color import Color
from log import Debug

class SecondHand:
    """ GUI widget for drawing the second hand of a clock """

    SECOND_RADIUS = 3
    SECOND_MARGIN = 2

    def __init__(self, tft, x, y, second=0):
        self._tft = tft
        self._x = x
        self._y = y
        self._second = second
        self._am = None
        self._radius = tft.width() // 2 - SecondHand.SECOND_RADIUS - SecondHand.SECOND_MARGIN
        self._initialized = False

    def init(self):
        if self._initialized:
            return
        
        for second in range(60):
            self._draw(second, Color.SECOND_BG_COLOR)

        self._initialized = True


    def update(self, second, am=True):
        if not self._initialized:
            self.init()

        if second == self._second and am == self._am:
            return

        # Clear the old second hand position
        self._draw(self._second, Color.SECOND_BG_COLOR)

        # Calculate new position based on seconds
        color = Color.SECOND_FG_COLOR_AM if am else Color.SECOND_FG_COLOR_PM
        self._draw(second, color)

        self._second = second
        self._am = am


    def _draw(self, second, color):
        angle = Util.second_to_angle(second % 60)
        x, y = Util.angle_to_xy(angle, self._radius)
        self._tft.fill_circle(self._x + int(x), self._y - int(y), self.SECOND_RADIUS, color)

