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
import uasyncio as asyncio
import utime
from machine import Pin, RTC

from lib_time import strptime

from pyprof import PyProf
from log import Debug
from app_event import AppEvent


class App(PyProf):
    ENABLE_FAST_SIMULATION = True
    ENABLE_FAST_SIMULATION = False

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):  # Prevent re-initialization on subsequent calls
            super().__init__()
            self._initialized = True
            self._rtc = RTC()
            self._is_rtc_initialized = False
            self._led = Pin(25,Pin.OUT)

    @classmethod
    def get_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    

    async def start(self, app_context):
        """ app task: it spawn gui task, wiznet task and timer task """

        Debug.log(f'{__class__.__name__}: start() ...')
        self._app_context = app_context
        self._handlers = {
            AppEvent.Timer1Hz: self._handler_timer1hz,
            AppEvent.SntpUpdate: self._handler_sntp_update,
        }

        asyncio.create_task(app_context.gui.start(app_context))

        if not App.ENABLE_FAST_SIMULATION:
            asyncio.create_task(app_context.wiznet.start(app_context))
            asyncio.create_task(self.timer_task(app_context))
        else:
            #######################################################################
            # simulate SNTP update for testing
            sntp_time = b'Sat Jul 12 00:00:00 2025' 
            await self.post_event(event=AppEvent.SntpUpdate, obj=sntp_time)
            #######################################################################

            asyncio.create_task(self.timer_fast_simulation_task(app_context))


        await super().message_loop_forever()



    async def _handler_sntp_update(self, msg):
        """ handling SNTP response => set RTC """
        Debug.log(f'{__class__.__name__}: handler_sntp_update: obj={msg.obj}')

        date_bytes = msg.obj
        date_str = date_bytes.decode('utf-8') 
        time_struct = strptime(date_str, '%a %b %d %H:%M:%S %Y') 
        Debug.log(f"{__class__.__name__}: {time_struct}")

        if time_struct is not None:
            year = time_struct[0] 
            month = time_struct[1]
            day = time_struct[2]
            hour = time_struct[3]
            minute = time_struct[4]
            second = time_struct[5]
            tm_wday = time_struct[6]
            tm_yday = time_struct[7]
            yymmdd = "{:02d}-{:02d}-{:02d}".format(year, month, day)
            hhmmss = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
            Debug.log(f"{__class__.__name__}: yyyy-mm-dd {yymmdd}")
            Debug.log(f"{__class__.__name__}: hh:mm:ss {hhmmss}")
            Debug.log(f"{__class__.__name__}: tm_wday={tm_wday}, tm_yday={tm_yday}")

            datetime = (year, month, day, tm_wday, hour, minute, second, 0)
            Debug.log(f"{__class__.__name__}: rtc.datetime({datetime})...")
            self._rtc.datetime(datetime)
            self._is_rtc_initialized = True
        else:
            Debug.log("{__class__.__name__}: Failed to parse time_struct")


    async def _handler_timer1hz(self, msg):
        """ Timer 1Hz handler: get time from RTC and post RtcUpdate event to Gui task """
        if self._is_rtc_initialized:

            datetime = self._rtc.datetime()
            Debug.log(f"{__class__.__name__}: rtc.datetime()={datetime}")
            await self._app_context.gui.post_event(event=AppEvent.RtcUpdate, obj=datetime)

        self._led.toggle()



    async def timer_task(self, app_context):
        """ generate timer event: 1Hz """
        while True:
            await asyncio.sleep(1)  # wait for 1 second
            await self.post_event(AppEvent.Timer1Hz)

    async def timer_fast_simulation_task(self, app_context):
        """ mock fast timer by increasing 1s every 0.1s """
        seconds = utime.time()
        Debug.log(f"{__class__.__name__}: seconds = {seconds}")

        while True:
            ###################################################################
            # test for seconds
            await asyncio.sleep(1)  # wait for 1 second
            seconds += 1
            ###################################################################

            ###################################################################
            # test hours and minutes
            # await asyncio.sleep(0.05)  # wait for 0.05 second
            # seconds += 60   
            ###################################################################


            datetime = utime.localtime(seconds)
            Debug.log(f"{__class__.__name__}: seconds={seconds}, datetime={datetime}")

            year = datetime[0] 
            month = datetime[1]
            day = datetime[2]
            hour = datetime[3]
            minute = datetime[4]
            second = datetime[5]
            tm_wday = datetime[6]
            tm_yday = datetime[7]
            datetime = (year, month, day, tm_wday, hour, minute, second, 0)
            Debug.log(f"{__class__.__name__}: rtc.datetime({datetime})...")
            self._rtc.datetime(datetime)

            await self.post_event(AppEvent.Timer1Hz)

