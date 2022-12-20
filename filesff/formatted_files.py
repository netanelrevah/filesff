from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Type

from filesff.files import FileHandle


@dataclass
class FileAccessor:
    handle: FileHandle

    def create_reader(self):
        return self.handle.create_unicode_reader()

    def create_writer(self):
        return self.handle.create_unicode_writer()

    def load(self, *args, **kwargs):
        raise NotImplementedError()

    def dump(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def open(cls, path: Path, file_handle_cls: Optional[Type[FileHandle]] = FileHandle) -> "FileAccessor":
        return cls(file_handle_cls.of(path))
