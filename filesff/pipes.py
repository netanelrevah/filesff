from dataclasses import dataclass
from os import PathLike
from pathlib import Path

from filesff.core.handlers import FileHandle
from filesff.paths import PathFileHandle


@dataclass
class PipeFileHandle(FileHandle):
    file_handle: FileHandle

    @classmethod
    def of_path(cls, path: Path):
        return cls(file_handle=PathFileHandle.of(path))

    @classmethod
    def of_str(cls, path: str | PathLike[str]):
        return cls(PathFileHandle.of_str(path))

    @classmethod
    def of_temp(cls):
        return cls(PathFileHandle.of_temp())
