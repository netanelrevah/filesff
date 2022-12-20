import errno
import os
from dataclasses import dataclass
from gzip import GzipFile
from pathlib import Path
from tempfile import NamedTemporaryFile


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
    FILE_NAME_EXTENSION = ""
    FILE_NAME_ADDITIONAL_EXTENSIONS = []

    pointer: FilePointer

    @property
    def extension(self):
        return self.FILE_NAME_EXTENSION

    def create_empty_file(self):
        if not self.pointer.path.exists():
            self.create_unicode_writer()

    def open(self, mode):
        return self.pointer.path.open(mode=mode)

    def create_writer(self, mode="w"):
        return self.open(mode)

    def create_reader(self, mode="r"):
        return self.open(mode)

    def create_unicode_writer(self):
        return self.create_writer(mode="w")

    def create_bytes_writer(self):
        return self.create_writer(mode="wb")

    def create_unicode_reader(self):
        self.create_empty_file()  # we must have at least empty file to create reader
        return self.create_reader(mode="r")

    def create_bytes_reader(self):
        self.create_empty_file()  # we must have at least empty file to create reader
        return self.create_reader(mode="rb")

    @classmethod
    def of(cls, path: Path):
        return cls(PathFilePointer(path))


class CompressedFileHandle(FileHandle):
    pass


class GzippedFileHandle(CompressedFileHandle):
    FILE_NAME_EXTENSION = ".gz"
    FILE_NAME_ADDITIONAL_EXTENSIONS = [".gzip"]

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
