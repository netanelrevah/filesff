import errno
import os
from dataclasses import dataclass
from gzip import GzipFile
from pathlib import Path


class FilePointer:
    @property
    def file_path(self):
        raise NotImplementedError()


@dataclass
class PathFilePointer(FilePointer):
    _file_path: Path

    @property
    def file_path(self) -> Path:
        return self._file_path


@dataclass
class FileHandle:
    FILE_NAME_EXTENSION = ""
    FILE_NAME_ADDITIONAL_EXTENSIONS = []
    COMPRESSED = False

    file_pointer: FilePointer

    @property
    def file_path(self):
        return self.file_pointer.file_path

    @property
    def extension(self):
        return self.FILE_NAME_EXTENSION

    @property
    def is_compressed(self):
        return self.COMPRESSED

    @property
    def file_size(self):
        return os.stat(self.file_path).st_size

    def create_empty_file(self):
        if not os.path.exists(self.file_path):
            self.create_writer()

    def create_writer(self, write_mode="wb"):
        return open(self.file_path, mode=write_mode)

    def create_reader(self):
        self.create_empty_file()  # we must have at least empty file to create reader
        return open(self.file_path, mode="rb")

    @classmethod
    def of(cls, file_path: Path):
        return cls(PathFilePointer(file_path))


class GzippedFileHandle(FileHandle):
    FILE_NAME_EXTENSION = ".gz"
    FILE_NAME_ADDITIONAL_EXTENSIONS = [".gzip"]
    COMPRESSED = True

    def create_writer(self, write_mode="wb"):
        return GzipFile(fileobj=super(GzippedFileHandle, self).create_writer(write_mode=write_mode))

    def create_reader(self):
        return GzipFile(fileobj=super(GzippedFileHandle, self).create_reader())


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
