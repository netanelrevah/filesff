from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Type

from filesff.files_handlers import FileHandle


@dataclass
class FileAccessor:
    handle: FileHandle

    def load(self):
        raise NotImplementedError()

    def dump(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def of(cls, file_path, file_handle_cls: Type[FileHandle] = FileHandle) -> "FileAccessor":
        return cls(file_handle_cls.of(file_path))

    @classmethod
    def of_temp(cls, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of_temp())
