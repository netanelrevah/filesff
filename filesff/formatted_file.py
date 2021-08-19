from typing import Optional, Type

from filesff.files import FileHandle


class FileAccessor:
    def __init__(self, file_handler: FileHandle):
        self.file_handler = file_handler

    @classmethod
    def open(cls, path: Optional[str] = None, file_handle: Optional[Type[FileHandle]] = FileHandle) -> "FileAccessor":
        if path is None:
            return cls(file_handle.new_temporary_file())
        return cls(file_handle.from_file_path(path))

    def get_writer(self, write_compressed_data=False):
        if write_compressed_data:
            return FileHandle.create_writer(self.file_handler)
        return self.file_handler.create_writer()

    def get_reader(self):
        return self.file_handler.create_reader()
