from dataclasses import dataclass
from os import PathLike
from typing import Any, List, Type

from filesff.core.formatters import FileFormatter, StringFormatter
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
class LinesFileAccessor(FileAccessor):
    handle: FileHandle
    formatter: StringFormatter

    def load(self):
        return list(self.lines())

    def dump(self, value: List[Any]):
        with self.handle.create_text_writer() as writer:
            for item in value:
                writer.write(self.formatter.dumps(item))
                writer.write("\n")

    def lines(self):
        with self.handle.create_text_reader() as reader:
            for line in reader:
                yield self.formatter.loads(line)

    @classmethod
    def of(
        cls,
        file_path: str | PathLike[str],
        formatter: StringFormatter,
        file_handle_cls: Type[FileHandle] = FileHandle,
    ):
        return cls(file_handle_cls.of(file_path), formatter)

    @classmethod
    def of_temp(cls, formatter: StringFormatter, file_handle_cls: Type[FileHandle] = FileHandle):
        return cls(file_handle_cls.of_temp(), formatter)
