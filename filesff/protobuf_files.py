from dataclasses import dataclass
from os import PathLike
from typing import Any, Type

from google.protobuf.json_format import MessageToJson, Parse

from filesff.file_accessors import FileAccessor
from filesff.files_handlers import FileHandle


@dataclass
class ProtoJsonFile(FileAccessor):
    handle: FileHandle
    message_cls: Any

    def load(self):
        return Parse(self.handle.create_text_reader().read(), message=self.message_cls())

    def dump(self, message):
        return self.handle.create_text_writer().write(MessageToJson(message))

    @classmethod
    def of(cls, file_path: str | PathLike[str], message_cls: Any, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of(file_path), message_cls)

    @classmethod
    def of_temp(cls, message_cls: Any, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of_temp(), message_cls)
