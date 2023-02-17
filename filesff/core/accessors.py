from contextlib import closing, contextmanager
from dataclasses import dataclass
from os import PathLike
from typing import Any, Generator, Iterator, List, Type

from filesff.core.formatters import FileFormatter, FullFileFormatter
from filesff.core.handlers import FileHandle


@dataclass
class FullFileAccessor:
    handle: FileHandle
    formatter: FullFileFormatter

    def load(self):
        with self.handle.create_text_reader() as reader:
            return self.formatter.load(reader)

    def dump(self, value: Any):
        with self.handle.create_text_writer() as writer:
            return self.formatter.dump(writer, value)

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
class FileAccessor:
    handle: FileHandle
    formatter: FileFormatter

    def load(self):
        with self.handle.create_text_reader() as reader:
            yield self.formatter.load(reader)

    def dump(self, value: List[Any]):
        with self.handle.create_text_reader() as writer:
            return self.formatter.dump(writer, value)

    @contextmanager
    def create_loader(self) -> Iterator[Any]:
        with self.handle.create_text_reader() as reader:
            yield self.formatter.create_loader(reader)

    @contextmanager
    def create_dumper(self, **kwargs):
        with self.handle.create_text_writer() as writer:
            return self.formatter.create_dumper(writer, **kwargs)

    @classmethod
    def of(
        cls,
        file_path: str | PathLike[str],
        formatter: FileFormatter,
        file_handle_cls: Type[FileHandle] = FileHandle,
    ):
        return cls(file_handle_cls.of(file_path), formatter)

    @classmethod
    def of_temp(cls, formatter: FileFormatter, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of_temp(), formatter)
