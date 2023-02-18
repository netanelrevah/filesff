from dataclasses import dataclass
from typing import IO, Any, AnyStr, Iterator

from google.protobuf.json_format import MessageToJson, Parse
from google.protobuf.message import Message

from filesff.core.formatters import FileFormatter, FullFileFormatter


@dataclass
class ProtoBytesFileFormatter(FullFileFormatter):
    def load(self, reader: IO, **kwargs) -> AnyStr:
        message_cls = kwargs["message_cls"]
        return message_cls.ParseFromString(reader.read())

    def dump(self, writer: IO, value: Any, **kwargs):
        writer.write(value.SerializeToString())


@dataclass
class ProtoJsonFileFormatter(FullFileFormatter):
    def load(self, reader: IO, **kwargs) -> AnyStr:
        message_cls = kwargs["message_cls"]
        return Parse(reader.read(), message=message_cls())

    def dump(self, writer: IO, value: Any, **kwargs):
        writer.write(MessageToJson(value))


@dataclass
class ProtoJsonLinesFileLoader:
    reader: IO
    message_cls: type[Message]

    def __iter__(self):
        for line in self.reader:
            yield Parse(line, message=self.message_cls())


@dataclass
class ProtoJsonLinesFileDumper:
    writer: IO

    def dump_message(self, message: Message):
        self.writer.write(MessageToJson(message, indent=0).replace("\n", "") + "\n")


@dataclass
class ProtoJsonLinesFileFormatter(FileFormatter, FullFileFormatter):
    def create_loader(self, reader: IO, **kwargs) -> ProtoJsonLinesFileLoader:
        message_cls = kwargs["message_cls"]
        return ProtoJsonLinesFileLoader(reader, message_cls=message_cls)

    def create_dumper(self, writer: IO, **_) -> ProtoJsonLinesFileDumper:
        return ProtoJsonLinesFileDumper(writer)

    def load(self, reader: IO, **kwargs) -> Iterator[Message]:
        loader = self.create_loader(reader, **kwargs)
        yield from loader

    def dump(self, writer: IO, value: Iterator[Message], **_):
        dumper = self.create_dumper(writer)
        for message in value:
            dumper.dump_message(message)
