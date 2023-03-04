from dataclasses import dataclass
from typing import Any, AnyStr, BinaryIO

import msgpack

from filesff.core.formatters import FullBinaryFileFormatter


@dataclass
class MsgPackFileFormatter(FullBinaryFileFormatter):
    def load(self, reader: BinaryIO, **kwargs) -> AnyStr:
        return msgpack.load(reader, **kwargs)

    def dump(self, writer: BinaryIO, value: Any, **kwargs):
        msgpack.dump(value, writer, **kwargs)
