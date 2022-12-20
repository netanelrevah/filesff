from typing import Any

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


class JsonFile(FileAccessor):
    FORMATTER = json

    def load(self):
        return self.FORMATTER.loads(self.handle.create_unicode_reader().read())

    def dump(self, value: Any):
        self.handle.create_unicode_writer().write(self.FORMATTER.dumps(value, indent=2))
