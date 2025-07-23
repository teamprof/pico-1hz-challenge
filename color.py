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

class Color:
    SCREEN_BG_COLOR = gc9a01.CYAN   # screen background color

    EYE_COLOR = gc9a01.WHITE        # eye color
    EYE_BORDER_COLOR = gc9a01.BLACK # eye border color
    PUPIL_COLOR = gc9a01.BLUE       # pupil color

    SECOND_FG_COLOR_AM = gc9a01.GREEN   # foreground color of the second hand in AM
    SECOND_FG_COLOR_PM = gc9a01.RED     # foreground color of the second hand in PM
    SECOND_BG_COLOR = gc9a01.color565(128,128,128)  # background color of the second hand (Gray)

    TEXT_FG_COLOR_AM = gc9a01.BLUE      # foreground color of the text in AM
    TEXT_FG_COLOR_PM = gc9a01.MAGENTA   # foreground color of the text in PM
