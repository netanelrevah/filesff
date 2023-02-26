from contextlib import contextmanager
from dataclasses import dataclass
from os import PathLike
from typing import Any, Iterator, Type

from filesff.core.formatters import (
    BinaryFileFormatter,
    FullBinaryFileFormatter,
    FullTextFileFormatter,
    TextFileFormatter,
)
from filesff.core.handlers import FileHandle


@dataclass
class FullFileAccessor:
    handle: FileHandle
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

    @classmethod
    def of(
        cls,
        file_path: str | PathLike[str],
        formatter: FullBinaryFileFormatter | FullTextFileFormatter,
        file_handle_cls: Type[FileHandle] = FileHandle,
    ):
        return cls(file_handle_cls.of(file_path), formatter)

    @classmethod
    def of_temp(
        cls, formatter: FullBinaryFileFormatter | FullTextFileFormatter, file_handle_cls: Type[FileHandle] = FileHandle
    ):
        return cls(file_handle_cls.of_temp(), formatter)


@dataclass
class FileAccessor(FullFileAccessor):
    handle: FileHandle
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
