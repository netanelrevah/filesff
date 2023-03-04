import bz2
import gzip
from dataclasses import dataclass
from os import PathLike
from typing import BinaryIO, TextIO, cast

from filesff.core.pointers import (
    FilePointer,
    FolderPointer,
    FSFilePointer,
    TemporaryFilePointer,
)

class S3KeyPointer(FilePointer):
    pass

class ReadableFileHandle:
    def create_binary_reader(self) -> BinaryIO:
        raise NotImplementedError()
    def create_text_reader(self) -> TextIO:
        raise NotImplementedError()
        
class WriteableFileHandle
    def create_binary_writer(self) -> BinaryIO:
        raise NotImplementedError()
    def create_text_writer(self) -> TextIO:
        raise NotImplementedError()

class OpenableFileHandle(FileHandle):
    def open(self, *args, **kwargs):
        raise NotImplementedError()

    def create_text_writer(self) -> TextIO:
        return self.open(mode="wt")

    def create_text_reader(self) -> TextIO:
        return self.open(mode="rt")

    def create_binary_writer(self) -> BinaryIO:
        return self.open(mode="wb")

    def create_binary_reader(self) -> BinaryIO:
        return self.open(mode="rb")


@dataclass
class PathFileHandle(OpenableFileHandle):
    pointer: FSFilePointer

    def open(self, mode) -> TextIO | BinaryIO:
        return open(self.pointer.path, mode=mode)
        
    def create_empty_file(self):
        if not self.pointer.path.exists():
            self.create_text_writer()

    @classmethod
    def of(cls, path: str | PathLike[str]):
        return cls(FSFilePointer.of(path))

    @classmethod
    def of_temp(cls):
        return cls(TemporaryFilePointer.create())


@dataclass
class PipeFileHandle(FileHandle):
    file_handle: FileHandle

    @classmethod
    def of_path(cls, path: str | PathLike[str]):
        return cls(file_handle=PathFileHandle.of(path))


class GzippedFileHandle(PipeFileHandle):
    def open(self, mode):
        return gzip.open(fileobj=self.file_handle.create_binary_reader())


class BZip2FileHandle(PipeFileHandle):
    def open(self, mode):
        return bz2.open(fileobj=self.file_handle.create_binary_reader(),mode)
