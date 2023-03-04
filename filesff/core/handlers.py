from io import TextIOWrapper
from typing import BinaryIO, TextIO


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
