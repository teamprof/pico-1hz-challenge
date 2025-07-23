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
from machine import Pin, SPI  

import gc9a01 as gc9a01 

from pyprof import PyProf
from eye import Eye
from second_hand import SecondHand
from digital_clock import DigitalClock
from color import Color
from util import Util
from log import Debug
from app_event import AppEvent


SCL_PIN = 10 
SDA_PIN = 11 
CS_PIN = 13
RST_PIN = 14 
DC_PIN = 15 

LCD_WIDTH = 240
LCD_HEIGHT = 240

EYE_Y_OFFSET = -20  

class Gui(PyProf):
    ROTATION = 0
    BUFFER_SIZE = 16*1024

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):  # Prevent re-initialization on subsequent calls
            super().__init__()
                    
            spi = SPI(1, baudrate=60000000, sck=Pin(SCL_PIN), mosi=Pin(SDA_PIN))
            tft = gc9a01.GC9A01(spi,240,240, 
                                dc=Pin(DC_PIN, Pin.OUT), 
                                cs=Pin(CS_PIN, Pin.OUT), 
                                reset=Pin(RST_PIN, Pin.OUT),
                                rotation=self.ROTATION,
                                buffer_size=self.BUFFER_SIZE)
            tft.init()

            self._tft = tft
            self._initialized = True

    @classmethod
    def get_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    
    async def start(self, app_context):
        """ gui task: it draws the clock and handles RTC updates """

        Debug.log(f'{__class__.__name__}: start() ...')
        self._app_context = app_context

        Debug.log(f"{__class__.__name__}: LCD width={self._tft.width()} height={self._tft.height()}")
        
        self._tft.fill(Color.SCREEN_BG_COLOR)

        left_eye_x = self._tft.width() // 2 - Eye.EYE_RADIUS - Eye.EYE_SPACING // 2
        right_eye_x = self._tft.width() // 2 + Eye.EYE_RADIUS + Eye.EYE_SPACING // 2
        eyes_y = self._tft.height() // 2 
        if DigitalClock.ENABLE_DIGITAL_CLOCK:
            eyes_y += EYE_Y_OFFSET
        self._left_eye = Eye(self._tft, left_eye_x, eyes_y)
        self._right_eye = Eye(self._tft, right_eye_x, eyes_y)
        Debug.log(f"{__class__.__name__}: left_eye_x={left_eye_x} right_eye_x={right_eye_x}, eyes_y={eyes_y}")

        second_hand_x = self._tft.width() // 2
        second_hand_y = self._tft.height() // 2
        self._second_hand = SecondHand(self._tft, second_hand_x, second_hand_y)

        self._digital_clock = DigitalClock(self._tft)

        self._left_eye.init()
        self._right_eye.init()
        self._second_hand.init()
        self._digital_clock.init()

        self._handlers = {
            AppEvent.RtcUpdate: self._handler_rtc_update,
        }
        await super().message_loop_forever()


    async def _handler_rtc_update(self, msg):
        # Debug.log(f'{__class__.__name__}: handler_rtc_update: obj={msg.obj}')

        datetime = msg.obj
        year = datetime[0] 
        month = datetime[1]
        day = datetime[2]
        hour = datetime[4]
        minute = datetime[5]
        second = datetime[6]
        tm_wday = datetime[3]
        millisecond = datetime[7]
        hhmmss = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
        Debug.log(f"{__class__.__name__}: {hhmmss}")
        
        angle_hour = Util.hour_to_angle(hour, minute) 
        angle_minute = Util.minute_to_angle(minute) 
        angle_second = Util.second_to_angle(second)

        hh_x, hh_y = Util.angle_to_xy(angle_hour, Eye.EYE_RADIUS - Eye.PUPIL_RADIUS - Eye.EYE_MARGIN)
        mm_x, mm_y = Util.angle_to_xy(angle_minute, Eye.EYE_RADIUS - Eye.PUPIL_RADIUS - Eye.EYE_MARGIN)

        self._left_eye.update_pupil(int(hh_x), int(hh_y))
        self._right_eye.update_pupil(int(mm_x), int(mm_y))
        self._second_hand.update(second, am=(hour < 12))
        self._digital_clock.update(hour, minute, second)




