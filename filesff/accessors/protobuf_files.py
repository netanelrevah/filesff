from dataclasses import dataclass
from os import PathLike
from typing import Any, Type

from google.protobuf.json_format import MessageToJson, Parse

from filesff.accessors.base import FileAccessor
from filesff.core.files_handlers import FileHandle


@dataclass
class AbstractProtobufFileAccessor(FileAccessor):

    handle: FileHandle
    message_cls: Any

    def load(self):
        raise NotImplementedError()

    def dump(self, value: Any):
        raise NotImplementedError()

    @classmethod
    def of(cls, file_path: str | PathLike[str], message_cls: Any, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of(file_path), message_cls)

    @classmethod
    def of_temp(cls, message_cls: Any, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of_temp(), message_cls)


@dataclass
class ProtobufFileAccessor(FileAccessor):
    handle: FileHandle
    message_cls: Any

    def load(self):
        with self.handle.create_text_reader() as reader:
            return self.message_cls.ParseFromString(reader.read())

    def dump(self, value):
        with self.handle.create_text_writer() as writer:
            return writer.write(value.SerializeToString())


@dataclass
class ProtoJsonFileAccessor(FileAccessor):
    handle: FileHandle
    message_cls: Any

    def load(self):
        with self.handle.create_text_reader() as reader:
            return Parse(reader.read(), message=self.message_cls())

    def dump(self, value):
        with self.handle.create_text_writer() as writer:
            return writer.write(MessageToJson(value))
