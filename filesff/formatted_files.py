from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Type

from filesff.files import FileHandle


@dataclass
class FileAccessor:
    file_handle: FileHandle

    def get_writer(self, write_compressed_data=False):
        if write_compressed_data:
            return FileHandle.create_writer(self.file_handle)
        return self.file_handle.create_writer()

    def get_reader(self):
        return self.file_handle.create_reader()

    @classmethod
    def open(cls, path: Path, file_handle: Optional[Type[FileHandle]] = FileHandle) -> "FileAccessor":
        return cls(file_handle.of(path))
