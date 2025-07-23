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
import vga1_16x32 as font

from color import Color
from log import Debug

class DigitalClock:
    """ GUI widget for showing a digital clock """

    ENABLE_DIGITAL_CLOCK = True
    # ENABLE_DIGITAL_CLOCK = False

    TIME_FORMAT = "{:02}:{:02}:{:02}"
    TEXT_Y_OFFSET = 38

    def __init__(self, tft, x=None, y=None):
        self._tft = tft
        self._x = x if x is not None else (tft.width() - (len("hh:mm:ss") * font.WIDTH)) // 2
        self._y = y if y is not None else tft.height() // 2 + self.TEXT_Y_OFFSET
        self._initialized = False

    def init(self):
        if self._initialized or not self.ENABLE_DIGITAL_CLOCK:
            return

        Debug.log(f"{__class__.__name__}: _x={self._x}, _y={self._y} font.WIDTH={font.WIDTH}, .HEIGHT={font.HEIGHT}")

        text_color = Color.TEXT_FG_COLOR_AM 
        self._tft.text(font, "hh:mm:ss", self._x, self._y, text_color, Color.SCREEN_BG_COLOR,)

        self._initialized = True


    def update(self, hour, minute, second):
        if not self.ENABLE_DIGITAL_CLOCK:
            return

        if not self._initialized:
            self.init()

        hhmmss = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
        text_color = Color.TEXT_FG_COLOR_AM if hour < 12 else Color.TEXT_FG_COLOR_PM
        self._tft.text(font, hhmmss, self._x, self._y, text_color, Color.SCREEN_BG_COLOR)
        Debug.log(f"{__class__.__name__}: {hhmmss}")
