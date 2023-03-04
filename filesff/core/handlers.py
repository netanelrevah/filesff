from io import TextIOWrapper
from typing import BinaryIO, TextIO

from filesff.core.accessors import FileAccessor, FullFileAccessor
from filesff.core.formatters import (
    BinaryFileFormatter,
    FullBinaryFileFormatter,
    FullTextFileFormatter,
    TextFileFormatter,
)


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
    def access(self, formatter: FullBinaryFileFormatter | FullTextFileFormatter) -> FullFileAccessor:
        if isinstance(formatter, BinaryFileFormatter) or isinstance(formatter, TextFileFormatter):
            return FileAccessor(self, formatter)
        return FullFileAccessor(self, formatter)


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
