# Copyright (c) 2023 Zeeland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/cushy-serial
# Contact Email: zeeland@foxmail.com

import serial
import logging

from serial.serialutil import *
from typing import Callable, List
from concurrent.futures import ThreadPoolExecutor

__all__ = ['CushySerial', 'enable_log']
logger = logging.getLogger(__name__)


def enable_log():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CushySerial(serial.Serial):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self._executor = ThreadPoolExecutor()
        self._callbacks: List[Callable] = []

    def send(self, msg: str or bytes):
        """
        send message to serial. You can input str or bytes data type as the message.
        """
        if not self.is_open:
            raise PortNotOpenError()
        if type(msg) == str:
            self.write(msg.encode())
        elif type(msg) == bytes:
            self.write(msg)
        self.flush()

    def on_message(self):
        """
        listen message from serial and register callback function. It will callback
        when serial receive message from serial.
        """
        if not self.is_open:
            raise PortNotOpenError()
        self._executor.submit(self._listen_thread)

        def decorator(func: Callable):
            self._callbacks.append(func)
            return func

        return decorator

    def _listen_thread(self):
        self.logger.debug("[cushy-serial] start to listen message")
        while True:
            res_msg: bytes = self.read_all()
            if res_msg:
                self.logger.debug(f"[cushy-serial] receive msg: {res_msg}")
                self._invoke_callbacks(res_msg)

    def _invoke_callbacks(self, msg: bytes):
        self.logger.debug("[cushy-serial] run callback task")
        for callback in self._callbacks:
            callback(msg)
            # self._executor.submit(callback, msg)
