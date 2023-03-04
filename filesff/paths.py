import os
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import BinaryIO, TextIO

from filesff.core.handlers import OpenableFileHandle
from filesff.core.pointers import FilePointer


@dataclass
class PathFilePointer(FilePointer):
    path: Path

    def exists(self):
        return self.path.exists()

    @classmethod
    def of_str(cls, path: str | PathLike[str]):
        return cls(Path(path))


@dataclass
class TemporaryFilePointer(PathFilePointer):
    should_delete: bool

    def __enter__(self) -> "TemporaryFilePointer":
        return self

    def delete(self):
        if not self.should_delete:
            return

        try:
            os.remove(self.path)
        except OSError:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def __del__(self):
        self.delete()

    @classmethod
    def create(cls, prefix=None, suffix=None, directory=None, delete=True) -> "TemporaryFilePointer":
        file_path = NamedTemporaryFile(prefix=prefix, suffix=suffix, dir=directory, delete=True).name

        return cls(Path(file_path), delete)


@dataclass
class PathFileHandle(OpenableFileHandle):
    pointer: PathFilePointer

    def open(self, mode, **kwargs) -> TextIO | BinaryIO:
        return open(self.pointer.path, mode=mode)

    def create_empty_file(self):
        if not self.pointer.path.exists():
            self.create_text_writer()

    @classmethod
    def of(cls, path: Path):
        return cls(PathFilePointer(path))

    @classmethod
    def of_str(cls, path: str | PathLike[str]):
        return cls(PathFilePointer.of_str(path))

    @classmethod
    def of_temp(cls):
        return cls(TemporaryFilePointer.create())
