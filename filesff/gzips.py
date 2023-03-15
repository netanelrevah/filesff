from gzip import GzipFile
from typing import BinaryIO, cast

from filesff.pipes import PipeFileHandle


class GzippedFileHandle(PipeFileHandle):
    def create_binary_reader(self) -> BinaryIO:
        return cast(
            BinaryIO,
            GzipFile(fileobj=self.file_handle.create_binary_reader(), mode="r"),
        )

    def create_binary_truncating_writer(self) -> BinaryIO:
        return cast(
            BinaryIO,
            GzipFile(fileobj=self.file_handle.create_binary_writer(), mode="w"),
        )
