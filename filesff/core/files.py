from contextlib import contextmanager
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Any, BinaryIO, Iterator, TextIO

from filesff.core.formatters import (
    BinaryFileFormatter,
    FullBinaryFileFormatter,
    FullTextFileFormatter,
    TextFileFormatter,
)


class FilePointer:
    pass


class FolderPointer:
    pass


class AccessibleFileHandle:
    def create_binary_reader(self) -> BinaryIO:
        raise NotImplementedError()

    def create_text_reader(self) -> TextIO:
        return TextIOWrapper(self.create_binary_reader())

    def create_binary_writer(self) -> BinaryIO:
        raise NotImplementedError()

    def create_text_writer(self) -> TextIO:
        return TextIOWrapper(self.create_binary_writer())

    def access(self, formatter: FullBinaryFileFormatter | FullTextFileFormatter) -> "FullFileAccessor":
        if isinstance(formatter, BinaryFileFormatter) or isinstance(formatter, TextFileFormatter):
            return FileAccessor(self, formatter)
        return FullFileAccessor(self, formatter)


@dataclass
class FullFileAccessor:
    handle: AccessibleFileHandle
    formatter: FullBinaryFileFormatter | FullTextFileFormatter

    def load(self, **kwargs):
        with self.handle.create_text_reader() as reader:
            return self.formatter.load(reader, **kwargs)

    def dump(self, value: Any, **kwargs):
        if isinstance(self.formatter, FullTextFileFormatter):
            with self.handle.create_text_writer() as writer:
                return self.formatter.dump(writer, value, **kwargs)
        if isinstance(self.formatter, FullBinaryFileFormatter):
            with self.handle.create_binary_reader() as writer:
                return self.formatter.dump(writer, value, **kwargs)
        raise TypeError()


@dataclass
class FileAccessor(FullFileAccessor):
    handle: AccessibleFileHandle
    formatter: BinaryFileFormatter | TextFileFormatter

    @contextmanager
    def create_loader(self, **kwargs) -> Iterator[Any]:
        if isinstance(self.formatter, TextFileFormatter):
            with self.handle.create_text_reader() as reader:
                yield self.formatter.create_loader(reader, **kwargs)
        if isinstance(self.formatter, BinaryFileFormatter):
            with self.handle.create_binary_reader() as reader:
                yield self.formatter.create_loader(reader, **kwargs)

    @contextmanager
    def create_dumper(self, **kwargs):
        with self.handle.create_text_writer() as writer:
            yield self.formatter.create_dumper(writer, **kwargs)
