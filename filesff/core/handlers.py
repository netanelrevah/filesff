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


class FileHandle:
    @property
    def pointer(self) -> FilePointer:
        raise NotImplementedError()

    def create_binary_writer(self) -> BinaryIO:
        raise NotImplementedError()

    def create_binary_reader(self) -> BinaryIO:
        raise NotImplementedError()

    def create_text_writer(self) -> TextIO:
        raise NotImplementedError()

    def create_text_reader(self) -> TextIO:
        raise NotImplementedError()


@dataclass
class FolderHandler:
    def get_file(self, file_pointer: FilePointer) -> FileHandle:
        raise NotImplementedError()

    def get_folder(self, folder_pointer: FolderPointer) -> "FolderHandler":
        raise NotImplementedError()


class OpenableFileHandle(FileHandle):
    def open(self, mode) -> TextIO | BinaryIO:
        raise NotImplementedError()

    def create_text_writer(self) -> TextIO:
        return cast(TextIO, self.open(mode="wt"))

    def create_text_reader(self) -> TextIO:
        return cast(TextIO, self.open(mode="rt"))

    def create_binary_writer(self) -> BinaryIO:
        return cast(BinaryIO, self.open(mode="wb"))

    def create_binary_reader(self) -> BinaryIO:
        return cast(BinaryIO, self.open(mode="rb"))


@dataclass
class FSFileHandle(OpenableFileHandle):
    _pointer: FSFilePointer

    @property
    def pointer(self) -> FilePointer:
        return self._pointer

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
class CompressedFileHandle(OpenableFileHandle):
    file_handle: FileHandle

    def create_compressed_reader(self) -> BinaryIO:
        return self.file_handle.create_binary_reader()

    def create_compressed_writer(self) -> BinaryIO:
        return self.file_handle.create_binary_writer()

    @classmethod
    def of(cls, path: str | PathLike[str]):
        return cls(file_handle=FSFileHandle.of(path))

    @classmethod
    def of_temp(cls):
        return cls(file_handle=FSFileHandle.of_temp())


class GzippedFileHandle(CompressedFileHandle):
    def open(self, mode):
        return gzip.open(self.file_handle.pointer.path, mode=mode)


class BZip2FileHandle(CompressedFileHandle):
    def open(self, mode):
        return bz2.open(self.file_handle.pointer.path, mode=mode)
