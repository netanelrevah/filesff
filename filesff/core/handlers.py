from bz2 import BZ2File
from dataclasses import dataclass
from gzip import GzipFile
from io import TextIOWrapper
from os import PathLike
from pathlib import Path
from typing import BinaryIO, TextIO, cast


class ReadableFileHandle:
    def create_binary_reader(self) -> BinaryIO:
        raise NotImplementedError()

    def create_text_reader(self) -> TextIO:
        return TextIOWrapper(self.create_binary_reader())


class WriteableFileHandle:
    def create_binary_writer(self) -> BinaryIO:
        raise NotImplementedError()

    def create_text_writer(self) -> TextIO:
        return TextIOWrapper(self.create_binary_writer())


class FileHandle(ReadableFileHandle, WriteableFileHandle):
    pass


class OpenableFileHandle(FileHandle):
    def open(self, mode, **kwargs):
        raise NotImplementedError()

    def create_text_writer(self) -> TextIO:
        return self.open(mode="wt")

    def create_binary_writer(self) -> BinaryIO:
        return self.open(mode="wb")

    def create_text_reader(self) -> TextIO:
        return self.open(mode="rt")

    def create_binary_reader(self) -> BinaryIO:
        return self.open(mode="rb")


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


class GzippedFileHandle(PipeFileHandle):
    def create_binary_reader(self) -> BinaryIO:
        return cast(
            BinaryIO,
            GzipFile(fileobj=self.file_handle.create_binary_reader(), mode="r"),
        )

    def create_binary_writer(self) -> BinaryIO:
        return cast(
            BinaryIO,
            GzipFile(fileobj=self.file_handle.create_binary_reader(), mode="w"),
        )


class BZip2FileHandle(PipeFileHandle, OpenableFileHandle):
    def create_binary_reader(self) -> BinaryIO:
        return cast(BinaryIO, BZ2File(filename=self.file_handle.create_binary_reader(), mode="r"))

    def create_binary_writer(self) -> BinaryIO:
        return cast(BinaryIO, BZ2File(filename=self.file_handle.create_binary_reader(), mode="w"))
