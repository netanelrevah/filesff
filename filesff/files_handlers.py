import errno
import os
from dataclasses import dataclass
from gzip import GzipFile
from os import PathLike
from pathlib import Path
from typing import IO, BinaryIO, TextIO, Union

from filesff.file_pointers import FilePointer, SimpleFilePointer, TemporaryFilePointer


@dataclass
class FileHandle:
    pointer: FilePointer

    def create_empty_file(self):
        if not self.pointer.path.exists():
            self.create_text_writer()

    def open(self, mode) -> Union[IO, TextIO, BinaryIO]:
        if "r" in mode:
            self.create_empty_file()
        return self.pointer.path.open(mode=mode)

    def create_text_writer(self) -> TextIO:
        return self.open(mode="w")

    def create_text_reader(self) -> TextIO:
        return self.open(mode="r")

    def create_bytes_writer(self) -> BinaryIO:
        return self.open(mode="wb")

    def create_bytes_reader(self) -> BinaryIO:
        return self.open(mode="rb")

    @classmethod
    def of(cls, path: str | PathLike[str]):
        return cls(SimpleFilePointer.of(path))

    @classmethod
    def of_temp(cls):
        return cls(TemporaryFilePointer.create())


class CompressedFileHandle(FileHandle):
    def create_compressed_reader(self):
        return self.create_bytes_reader()

    def create_compressed_writer(self):
        return self.create_bytes_writer()


class GzippedFileHandle(CompressedFileHandle):
    def open(self, mode):
        return GzipFile(fileobj=super(GzippedFileHandle, self).open(mode=mode))
