from contextlib import closing
from dataclasses import dataclass
from os import PathLike
from typing import Any, Generator, Iterator, List, Type

from filesff.core.formatters import ContinuesFileFormatter, FileFormatter
from filesff.core.handlers import FileHandle


@dataclass
class FileAccessor:
    handle: FileHandle
    formatter: FileFormatter

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
        formatter: FileFormatter,
        file_handle_cls: Type[FileHandle] = FileHandle,
    ):
        return cls(file_handle_cls.of(file_path), formatter)

    @classmethod
    def of_temp(cls, formatter: FileFormatter, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of_temp(), formatter)


@dataclass
class ContinuousFileAccessor(FileAccessor):
    handle: FileHandle
    formatter: ContinuesFileFormatter

    def load(self):
        return list(self.load_continuously())

    def dump(self, value: List[Any]):
        with closing(self.dump_continuously()) as lines_dumper:
            for item in value:
                lines_dumper.send(item)

    def load_continuously(self) -> Iterator[Any]:
        with self.handle.create_text_reader() as reader:
            yield from self.formatter.load_continuously(reader)

    def dump_continuously(self) -> Generator[None, Any, None]:
        with self.handle.create_text_writer() as writer:
            yield from self.formatter.dump_continuously(writer)

    @classmethod
    def of(
        cls,
        file_path: str | PathLike[str],
        formatter: ContinuesFileFormatter,
        file_handle_cls: Type[FileHandle] = FileHandle,
    ):
        return cls(file_handle_cls.of(file_path), formatter)

    @classmethod
    def of_temp(cls, formatter: ContinuesFileFormatter, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of_temp(), formatter)
