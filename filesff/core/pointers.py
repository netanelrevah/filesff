import os
from dataclasses import dataclass
from os import PathLike
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


class FolderPointer:
    pass


@dataclass
class FSFilePointer(FilePointer):
    _path: Path

    @property
    def path(self) -> Path:
        return self._path

    @classmethod
    def of(cls, path: str | PathLike[str]):
        return cls(Path(path))


@dataclass
class TemporaryFilePointer(FSFilePointer):
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
