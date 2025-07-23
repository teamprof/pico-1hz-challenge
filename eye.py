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

from color import Color
from log import Debug

class Eye:
    """ GUI widget of drawing an eye with a pupil """

    EYE_RADIUS = 45
    PUPIL_RADIUS = 8

    EYE_SPACING = 6
    EYE_MARGIN = 3

    def __init__(self, tft, x, y, pupil_x=0, pupil_y=0):
        self._tft = tft
        self._x = x
        self._y = y
        self._pupil_x = pupil_x 
        self._pupil_y = pupil_y 
        self._initialized = False

    def init(self):
        if self._initialized:
            return
        
        self._tft.circle(self._x, self._y, Eye.EYE_RADIUS, Color.EYE_BORDER_COLOR)
        self._tft.fill_circle(self._x, self._y, Eye.EYE_RADIUS-1, Color.EYE_COLOR)

        self._draw(self._x + self._pupil_x, self._y + self._pupil_y, Color.PUPIL_COLOR)
        
        self._initialized = True


    def update_pupil(self, x, y):
        if not self._initialized:
            self.init()

        if self._x == x and self._y == y:
            return

        # Clear the old pupil position
        self._draw(self._x + self._pupil_x, self._y - self._pupil_y, Color.EYE_COLOR)

        # Draw the new pupil position
        self._draw(self._x + x, self._y - y, Color.PUPIL_COLOR)

        # Update pupil position
        self._pupil_x = x
        self._pupil_y = y


    def _draw(self, x, y, color):
        self._tft.fill_circle(x, y, Eye.PUPIL_RADIUS, color)
