import errno
import os
import tempfile
from dataclasses import Field, dataclass
from gzip import GzipFile
from pathlib import Path
from typing import IO, Union


class FilePointerInterface:
    @property
    def file_path(self) -> Path:
        raise NotImplementedError()

    @property
    def file_path_str(self) -> str:
        raise NotImplementedError()


@dataclass
class FilePointer(FilePointerInterface):
    _file_path: Path

    def __init__(self, file_path: Union[str, Path]):
        self._file_path = Path(file_path)

    @property
    def file_path_str(self) -> str:
        return str(self._file_path)

    @property
    def file_path(self) -> Path:
        return self._file_path


@dataclass()
class TemporaryFilePointer(FilePointer):
    delete: bool = True

    def __init__(
        self,
        delete: bool = True,
        prefix: str = "",
        suffix: str = "",
        file_extension: str = "",
        directory: Union[Path, str] = None,
    ):
        self.delete = delete

        super().__init__(
            Path(
                tempfile.NamedTemporaryFile(
                    delete=True,  # don't be confused with the self.delete because here we need only the path!
                    prefix=prefix,
                    suffix=suffix + file_extension,
                    dir=Path(directory) if directory else None,
                ).name
            )
        )

    def __del__(self):
        if not self.delete:
            return

        try:
            os.remove(self.file_path)
        except OSError:
            pass


@dataclass
class FileHandle:
    FILE_NAME_EXTENSION = ""

    pointer: FilePointerInterface

    @property
    def file_path(self) -> Path:
        return self.pointer.file_path

    @property
    def file_path_str(self) -> str:
        return self.pointer.file_path_str

    @property
    def extension(self) -> str:
        return self.FILE_NAME_EXTENSION

    @property
    def is_compressed(self) -> bool:
        return False

    @property
    def file_size(self) -> int:
        return self.file_path.stat().st_size

    def create_empty_file(self):
        """
        initialize empty file in the path of the pointer if the file not exists
        """
        if not self.file_path.exists():
            self.create_writer()

    def create_writer(self, write_mode="w") -> IO:
        return open(self.file_path, mode=write_mode)

    def create_reader(self) -> IO:
        self.create_empty_file()  # we must have at least empty file to create reader
        return open(self.file_path, mode="r")

    @classmethod
    def new_temporary_file(cls, delete=True, prefix="", suffix="", directory=None) -> "FileHandle":
        return cls(
            TemporaryFilePointer(
                delete=delete, prefix=prefix, suffix=suffix, file_extension=cls.FILE_NAME_EXTENSION, directory=directory
            )
        )

    @classmethod
    def from_file_path(cls, file_path: Union[str, Path]) -> "FileHandle":
        return cls(FilePointer(file_path))


class GzippedFileHandle(FileHandle):
    FILE_NAME_EXTENSION = ".gz"

    def is_compressed(self):
        return True

    def create_writer(self, write_mode="w") -> GzipFile:
        return GzipFile(fileobj=super().create_writer(write_mode=write_mode))

    def create_reader(self) -> GzipFile:
        return GzipFile(fileobj=super().create_reader())


def create_directory_if_absence(file_path: Union[str, Path]):
    """
    python2.7 doesn't have exist_ok option so this supplies the same logic
    """
    file_path = Path(file_path)
    dir_name = file_path.parent
    if not dir_name.exists():
        try:
            dir_name.mkdir(parents=True, exist_ok=True)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
