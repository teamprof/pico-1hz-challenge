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
import math 

class Util:
    ANGLE_OFFSET = 0.0  # Offset for converting hh/mm/ss to angle 

    @staticmethod
    def hour_to_angle(hour, minute):
        return float(hour) / 12.0 * 360 + float(minute) / (12.0 * 60.0) * 360.0 + Util.ANGLE_OFFSET

    @staticmethod
    def minute_to_angle(minute):
        return float(minute) / 60.0 * 360.0  + Util.ANGLE_OFFSET

    @staticmethod
    def second_to_angle(second):
        return float(second) / 60.0 * 360.0  + Util.ANGLE_OFFSET


    @staticmethod
    def angle_to_xy(angle_degrees, radius=1): 
        angle_radians = math.radians(angle_degrees)  # Convert degrees to radians 
        x = radius * math.sin(angle_radians) 
        y = radius * math.cos(angle_radians) 
        return (x, y) 
