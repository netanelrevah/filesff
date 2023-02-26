from abc import ABC
from typing import Any, BinaryIO, TextIO


class FullBinaryFileFormatter:
    def load(self, reader: BinaryIO, **kwargs) -> Any:
        raise NotImplementedError()

    def dump(self, writer: BinaryIO, value: Any, **kwargs):
        raise NotImplementedError()


class BinaryFileFormatter(FullBinaryFileFormatter, ABC):
    def create_loader(self, reader: BinaryIO, **kwargs):
        raise NotImplementedError()

    def create_dumper(self, writer: BinaryIO, **kwargs):
        raise NotImplementedError()


class FullTextFileFormatter:
    def load(self, reader: TextIO, **kwargs) -> Any:
        raise NotImplementedError()

    def dump(self, writer: TextIO, value: Any, **kwargs):
        raise NotImplementedError()


class TextFileFormatter(FullTextFileFormatter, ABC):
    def create_loader(self, reader: TextIO, **kwargs):
        raise NotImplementedError()

    def create_dumper(self, writer: TextIO, **kwargs):
        raise NotImplementedError()
