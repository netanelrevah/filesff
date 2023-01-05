from dataclasses import dataclass
from typing import IO, Any, AnyStr, Optional, Text, TextIO

from filesff.files_handlers import FileHandle

try:
    import ujson as json
except ImportError:
    import json

from filesff.file_accessors import FileAccessor


class JsonFormatter:
    def load(self, file_object: IO) -> Text:
        raise NotImplementedError()

    def dump(self, value: Any, file_object: TextIO, indent: Optional[int]):
        raise NotImplementedError()

    def dumps(self, value: Any):
        raise NotImplementedError()

    def loads(self, text: AnyStr):
        raise NotImplementedError()


class JsonSerializable:
    @classmethod
    def from_dict(cls, value):
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()

    @classmethod
    def loads(cls, value):
        return cls.from_dict(json.loads(value))

    def dumps(self):
        return json.dumps(self.to_dict())


@dataclass
class JsonFile(FileAccessor):
    handle: FileHandle
    formatter: JsonFormatter = json

    def load(self):
        return self.formatter.load(self.handle.create_text_reader())

    def dump(self, value: Any):
        self.formatter.dump(self.handle.create_text_writer(), value, indent=2)
