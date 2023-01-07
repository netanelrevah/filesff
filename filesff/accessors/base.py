from dataclasses import dataclass
from typing import Any

from filesff.core.files_handlers import FileHandle


@dataclass
class FileAccessor:
    handle: FileHandle

    def load(self):
        raise NotImplementedError()

    def dump(self, value: Any):
        raise NotImplementedError()
