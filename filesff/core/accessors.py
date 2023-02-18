from contextlib import contextmanager
from dataclasses import dataclass
from os import PathLike
from typing import Any, Iterator, Type

from filesff.core.formatters import FileFormatter, FullFileFormatter
from filesff.core.handlers import FileHandle


@dataclass
class FullFileAccessor:
    handle: FileHandle
    formatter: FullFileFormatter

    def load(self, **kwargs):
        with self.handle.create_text_reader() as reader:
            return self.formatter.load(reader, **kwargs)

    def dump(self, value: Any, **kwargs):
        with self.handle.create_text_writer() as writer:
            return self.formatter.dump(writer, value, **kwargs)

    @classmethod
    def of(
        cls,
        file_path: str | PathLike[str],
        formatter: FullFileFormatter,
        file_handle_cls: Type[FileHandle] = FileHandle,
    ):
        return cls(file_handle_cls.of(file_path), formatter)

    @classmethod
    def of_temp(cls, formatter: FullFileFormatter, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of_temp(), formatter)


@dataclass
class FileAccessor(FullFileAccessor):
    handle: FileHandle
    formatter: FileFormatter

    @contextmanager
    def create_loader(self, **kwargs) -> Iterator[Any]:
        with self.handle.create_text_reader() as reader:
            yield self.formatter.create_loader(reader, **kwargs)

    @contextmanager
    def create_dumper(self, **kwargs):
        with self.handle.create_text_writer() as writer:
            yield self.formatter.create_dumper(writer, **kwargs)
