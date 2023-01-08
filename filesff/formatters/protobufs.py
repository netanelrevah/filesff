from abc import ABC
from dataclasses import dataclass
from typing import IO, Any, AnyStr

from google.protobuf.json_format import MessageToJson, Parse

from filesff.core.formatters import FileFormatter


class ProtobufFileFormatter(FileFormatter, ABC):
    message_cls: Any


@dataclass
class ProtoBytesFileFormatter(ProtobufFileFormatter):
    message_cls: Any

    def load(self, reader: IO) -> AnyStr:
        return self.message_cls.ParseFromString(reader.read())

    def dump(self, writer: IO, value: Any):
        writer.write(value.SerializeToString())


@dataclass
class ProtoJsonFileFormatter(ProtobufFileFormatter):
    message_cls: Any

    def load(self, reader: IO) -> AnyStr:
        return Parse(reader.read(), message=self.message_cls())

    def dump(self, writer: IO, value: Any):
        writer.write(MessageToJson(value))
