from dataclasses import dataclass
from typing import Any, AnyStr, BinaryIO

import msgpack

from filesff.core.accessors import FileAccessor
from filesff.core.formatters import FullBinaryFileFormatter
from filesff.paths import PathFileHandle


@dataclass
class MsgPackFileFormatter(FullBinaryFileFormatter):
    def load(self, reader: BinaryIO, **kwargs) -> AnyStr:
        return msgpack.load(reader, **kwargs)

    def dump(self, writer: BinaryIO, value: Any, **kwargs):
        msgpack.dump(value, writer, **kwargs)


def msgpack_file_accessor(file_path, file_handle_cls=PathFileHandle):
    return FileAccessor.of_path(
        file_path=file_path,
        formatter=MsgPackFileFormatter(),
        file_handle_cls=file_handle_cls,
    )


def temp_msgpack_file_accessor(file_handle_cls=PathFileHandle):
    return FileAccessor.of_temp(
        formatter=MsgPackFileFormatter(),
        file_handle_cls=file_handle_cls,
    )
