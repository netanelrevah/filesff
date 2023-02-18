from abc import ABC
from typing import IO, Any


class FullFileFormatter:
    def load(self, reader: IO, **kwargs) -> Any:
        raise NotImplementedError()

    def dump(self, writer: IO, value: Any, **kwargs):
        raise NotImplementedError()


class FileFormatter(FullFileFormatter, ABC):
    def create_loader(self, reader: IO, **kwargs):
        raise NotImplementedError()

    def create_dumper(self, writer: IO, **kwargs):
        raise NotImplementedError()
