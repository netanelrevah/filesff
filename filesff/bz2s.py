from bz2 import BZ2File
from typing import BinaryIO, cast

from filesff.pipes import PipeFileHandle


class BZip2FileHandle(PipeFileHandle):
    def create_binary_reader(self) -> BinaryIO:
        return cast(BinaryIO, BZ2File(filename=self.file_handle.create_binary_reader(), mode="r"))

    def create_binary_writer(self) -> BinaryIO:
        return cast(BinaryIO, BZ2File(filename=self.file_handle.create_binary_reader(), mode="w"))
