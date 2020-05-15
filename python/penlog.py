# SPDX-License-Identifier: Apache-2.0

import json
import socket
import sys
from datetime import datetime
from enum import Enum
from typing import Dict, TextIO


class MessageType(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    SUMMARY = "summary"
    READ = "read"
    WRITE = "write"
    PREAMBLE = "preamble"


class Logger:
    def __init__(self, component: str = "root", timefmt: str = '%c',
                 flush: bool = False, file_: TextIO = sys.stderr):
        self.host = socket.gethostname()
        self.component = component
        self.flush = flush
        self.file = file_

    def _log(self, msg: Dict) -> None:
        msg["component"] = self.component
        msg["host"] = self.host
        msg["timestamp"] = datetime.now().isoformat()
        print(json.dumps(msg), file=self.file, flush=self.flush)

    def log_preamble(self, data: str) -> None:
        msg = {
            'host': self.host,
            'type': MessageType.PREAMBLE,
            'data': data,
        }
        self._log(msg)

    def log_read(self, data: str, handle: str) -> None:
        msg = {
            'type': MessageType.READ,
            'handle': handle,
            'data': data,
        }
        self._log(msg)

    def log_write(self, data: str, handle: str) -> None:
        msg = {
            'type': MessageType.WRITE,
            'handle': handle,
            'data': data,
        }
        self._log(msg)

    def log_msg(self, data: str, type_: MessageType = MessageType.INFO) -> None:
        msg = {
            'type': type_,
            'data': data,
        }
        self._log(msg)

    def log_debug(self, data: str) -> None:
        self.log_msg(data, MessageType.DEBUG)

    def log_info(self, data: str) -> None:
        self.log_msg(data, MessageType.INFO)

    def log_warning(self, data: str) -> None:
        self.log_msg(data, MessageType.WARNING)

    def log_error(self, data: str) -> None:
        self.log_msg(data, MessageType.ERROR)

    def log_summary(self, data: str) -> None:
        self.log_msg(data, MessageType.SUMMARY)


# This is the module level default logger.
_logger = Logger()


def set_options(component: str = 'root', timefmt: str = '%c') -> None:
    global _logger
    _logger = Logger(component=component, timefmt=timefmt)


def log_preamble(data: str) -> None:
    _logger.log_preamble(data)


def log_msg(data: str, type_: MessageType = MessageType.INFO) -> None:
    _logger.log_msg(data)


def log_write(data: str, handle: str) -> None:
    _logger.log_write(data, handle)


def log_read(data: str, handle: str) -> None:
    _logger.log_read(data, handle)


def log_debug(data: str) -> None:
    log_msg(data, MessageType.DEBUG)


def log_info(data: str) -> None:
    log_msg(data, MessageType.INFO)


def log_warning(data: str) -> None:
    log_msg(data, MessageType.WARNING)


def log_error(data: str) -> None:
    log_msg(data, MessageType.ERROR)


def log_summary(data: str) -> None:
    log_msg(data, MessageType.SUMMARY)
