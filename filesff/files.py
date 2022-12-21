import errno
import os
from dataclasses import dataclass
from gzip import GzipFile
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import IO, BinaryIO, TextIO, Union


class FilePointer:
    @property
    def path(self) -> Path:
        raise NotImplementedError()

    @property
    def size(self):
        return self.path.stat().st_size

    def exists(self):
        return self.path.exists()


@dataclass
class PathFilePointer(FilePointer):
    _path: Path

    @property
    def path(self) -> Path:
        return self._path


@dataclass
class TemporaryFilePointer(PathFilePointer):
    should_delete: bool

    def __enter__(self) -> "TemporaryFilePointer":
        return self

    def delete(self):
        if not self.should_delete:
            return

        try:
            os.remove(self.path)
        except OSError:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def __del__(self):
        self.delete()

    @classmethod
    def create(cls, prefix=None, suffix=None, directory=None, delete=True) -> "TemporaryFilePointer":
        file_path = NamedTemporaryFile(prefix=prefix, suffix=suffix, dir=directory, delete=True).name

        return cls(Path(file_path), delete)


@dataclass
class FileHandle:
    pointer: FilePointer

    def create_empty_file(self):
        if not self.pointer.path.exists():
            self.create_writer()

    def open(self, mode) -> Union[IO, TextIO, BinaryIO]:
        if "r" in mode:
            self.create_empty_file()
        return self.pointer.path.open(mode=mode)

    def create_writer(self) -> IO:
        raise NotImplementedError()

    def create_reader(self) -> IO:
        raise NotImplementedError()

    @classmethod
    def of(cls, path: Path):
        return cls(PathFilePointer(path))


@dataclass
class TextFileHandle(FileHandle):
    def create_writer(self) -> TextIO:
        return self.open(mode="w")

    def create_reader(self) -> TextIO:
        return self.open(mode="r")


@dataclass
class BytesFileHandle(FileHandle):
    def create_writer(self) -> BinaryIO:
        return self.open(mode="wb")

    def create_reader(self) -> BinaryIO:
        return self.open(mode="rb")


class CompressedFileHandle(BytesFileHandle):
    def create_compressed_reader(self):
        return self.create_reader()

    def create_compressed_writer(self):
        return self.create_writer()


class GzippedFileHandle(CompressedFileHandle):
    def open(self, mode):
        return GzipFile(fileobj=super(GzippedFileHandle, self).open(mode=mode))


def create_directory_if_absence(file_path):
    """
    python2.7 doesn't have exist_ok option so this supplies the same logic
    """
    dir_name = os.path.dirname(file_path)

    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
