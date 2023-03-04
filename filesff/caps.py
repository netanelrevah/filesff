from dataclasses import dataclass
from typing import BinaryIO, Iterator, Sequence

from cap import CapFileDumper, CapFileLoader, CapturedPacket

from filesff.core.accessors import FileAccessor
from filesff.core.formatters import BinaryFileFormatter
from filesff.core.handlers import PathFileHandle


@dataclass
class CapFileFormatter(BinaryFileFormatter):
    def create_loader(self, reader: BinaryIO, **_) -> CapFileLoader:
        return CapFileLoader(reader)

    def create_dumper(self, writer: BinaryIO, **kwargs) -> CapFileDumper:
        return CapFileDumper(writer, **kwargs)

    def load(self, reader: BinaryIO, **_) -> Iterator[CapturedPacket]:
        loader = self.create_loader(reader)
        yield from loader

    def dump(self, writer: BinaryIO, value: Sequence[CapturedPacket], **kwargs):
        dumper = self.create_dumper(writer, **kwargs)
        dumper.dump_header()
        for captured_packet in value:
            dumper.dump_packet(captured_packet)


def cap_file_accessor(file_path, file_handle_cls=PathFileHandle):
    return FileAccessor.of_path(
        file_path=file_path,
        formatter=CapFileFormatter(),
        file_handle_cls=file_handle_cls,
    )


def temp_cap_file_accessor(file_handle_cls=PathFileHandle):
    return FileAccessor.of_temp(
        formatter=CapFileFormatter(),
        file_handle_cls=file_handle_cls,
    )
