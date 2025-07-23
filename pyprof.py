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
import queue
from app_message import AppMessage
from log import Debug

class PyProf:
    def __init__(self, queue_size=16):
        self._queue = queue.Queue(queue_size)
        self._handlers = {}

    async def post_event(self, event, arg0=0, arg1=0, obj=None):
        """ post event """
        msg = AppMessage(event, arg0, arg1, obj)
        await self._queue.put(msg)

    async def on_message(self, msg):
        """ route message to handler """
        if msg.event in self._handlers:
            await self._handlers[msg.event](msg)
        else:
            self._unsupportedHandler(msg)

    async def message_loop_forever(self):
        """ infinte loop to handle messages """
        while True:
            msg = await self._queue.get()
            await self.on_message(msg)
            
    def _unsupportedHandler(self, msg):
        Debug.log(f'unsupported event={msg.event}, arg0={msg.arg0}, arg1={msg.arg1}, obj={msg.obj}')
