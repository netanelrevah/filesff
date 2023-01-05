from dataclasses import dataclass
from typing import Any

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
