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
from machine import UART, Pin 

from lib_wiznet.adafruit_wizfiatcontrol import WizFi_ATcontrol

from app_event import AppEvent
from pyprof import PyProf
from log import Debug

import secrets

# hardware configuration
PORT = 1
RX = 5 
TX = 4 
resetpin = 20 
rtspin = False

# UART buffer sizes
UART_Tx_BUFFER_LENGTH = 128
UART_Rx_BUFFER_LENGTH = 128*2

TIMEZONE = 8  # HK: GMT+8
NTP_SERVER = "hk.pool.ntp.org"
# NTP_SERVER = "pool.ntp.org"
# NTP_SERVER = "time.google.com"

# debug flag
WIZFI_DEBUG = False



class Wiznet(PyProf):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):  # Prevent re-initialization on subsequent calls
            super().__init__()
            self._initialized = True

    @classmethod
    def get_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    

    async def start(self, app_context):
        """ wiznet task: """
        """ 1. connects to WiFi AP """
        """ 2. configures SNTP """
        """ 3. gets time from SNTP server """
        """ 4. posts SNTP time to app task """

        Debug.log(f'{__class__.__name__}: start() ...')
        self._app_context = app_context
        self._handlers = {
        }

        uart = UART(PORT, 115200, tx= Pin(TX), rx= Pin(RX), txbuf=UART_Tx_BUFFER_LENGTH, rxbuf=UART_Rx_BUFFER_LENGTH)
        wizfi = WizFi_ATcontrol( uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=WIZFI_DEBUG )

        Debug.log(f"{__class__.__name__}: WizFi360 firmware version: {wizfi.version}")
        Debug.log(f"{__class__.__name__}: Resetting WizFi360 module")
        wizfi.hard_reset()

        # connect to WiFi AP
        while not wizfi.is_connected:
            try:
                Debug.log(f"{__class__.__name__}: Connecting to AP {secrets.wifi['ssid']} ...")
                wizfi.connect(dict(secrets.wifi))
                continue
            except Exception as e:
                Debug.log(f"{__class__.__name__}: wiznet exception: {e}")
                while not wizfi.sync():
                    await asyncio.sleep(1)

            await asyncio.sleep(1)
        Debug.log(f"{__class__.__name__}: WiFi connected, local_ip: {wizfi.local_ip}")

        # configure SNTP
        try:
            Debug.log(f"{__class__.__name__}: Connecting to NTP server {NTP_SERVER} ...")
            wizfi.sntp_config(True, TIMEZONE, NTP_SERVER)
        except Exception as e:
            Debug.log(f"{__class__.__name__}: wiznet exception: {e}")
            while not wizfi.sync():
                await asyncio.sleep(1)

        # get SNTP time
        sntp_time = None
        while sntp_time is None:
            try:
                sntp_time = wizfi.sntp_time
                Debug.log(f"{__class__.__name__}: sntp_time: {sntp_time}")
                continue
            except Exception as e:
                Debug.log(f"{__class__.__name__}: wiznet exception: {e}")
                while not wizfi.sync():
                    await asyncio.sleep(1)
            await asyncio.sleep(1) 

        await app_context.app.post_event(event=AppEvent.SntpUpdate, obj=sntp_time)

        await super().message_loop_forever()


