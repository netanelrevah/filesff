import gzip
from dataclasses import dataclass
from os import PathLike
from typing import IO, BinaryIO, TextIO, Union

from filesff.core.pointers import FilePointer, SimpleFilePointer, TemporaryFilePointer


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
        return self.open(mode="wt")

    def create_text_reader(self) -> TextIO:
        return self.open(mode="rt")

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
        return super().open("rb")

    def create_compressed_writer(self):
        return super().open("wb")


class GzippedFileHandle(CompressedFileHandle):
    def open(self, mode):
        return gzip.open(self.pointer.path, mode=mode)
