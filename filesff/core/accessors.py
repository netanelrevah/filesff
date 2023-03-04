from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator

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
