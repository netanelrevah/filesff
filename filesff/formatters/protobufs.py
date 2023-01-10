from abc import ABC
from dataclasses import dataclass
from typing import IO, Any, AnyStr, Generator, Iterator

from google.protobuf.json_format import MessageToJson, Parse
from google.protobuf.message import Message

from filesff.core.formatters import ContinuesFileFormatter, FileFormatter


@dataclass
class ProtoBytesFileFormatter(FileFormatter):
    message_cls: Any

    def load(self, reader: IO) -> AnyStr:
        return self.message_cls.ParseFromString(reader.read())

    def dump(self, writer: IO, value: Any):
        writer.write(value.SerializeToString())


@dataclass
class ProtoJsonFileFormatter(FileFormatter):
    message_cls: Any

    def load(self, reader: IO) -> AnyStr:
        return Parse(reader.read(), message=self.message_cls())

    def dump(self, writer: IO, value: Any):
        writer.write(MessageToJson(value))


@dataclass
class ProtoJsonLinesFileFormatter(ContinuesFileFormatter):
    message_cls: Any

    def load_continuously(self, reader: IO) -> Iterator[Message]:
        for line in reader:
            yield Parse(line, message=self.message_cls())

    def dump_continuously(self, writer: IO) -> Generator[None, Message, None]:
        while True:
            message = yield None
            writer.write(MessageToJson(message, indent=0))
            writer.write("\n")
