from dataclasses import dataclass
from typing import Any

from filesff.files import TextFileHandle

try:
    import ujson as json
except ImportError:
    import json

from filesff.formatted_files import FileAccessor


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
    FORMATTER = json

    handle: TextFileHandle

    def load(self):
        return self.FORMATTER.loads(self.handle.create_reader().read())

    def dump(self, value: Any):
        self.handle.create_writer().write(self.FORMATTER.dumps(value, indent=2))
