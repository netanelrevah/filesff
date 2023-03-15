from dataclasses import dataclass
from typing import BinaryIO, Sequence

from cap import CapFileDumper, CapFileLoader, CapturedPacket

from filesff.core.formatters import BinaryFileFormatter


@dataclass
class CapFileFormatter(BinaryFileFormatter):
    def create_loader(self, reader: BinaryIO, **_) -> CapFileLoader:
        return CapFileLoader(reader)

    def create_dumper(self, writer: BinaryIO, **kwargs) -> CapFileDumper:
        return CapFileDumper(writer, **kwargs)

    def load(self, reader: BinaryIO, **_) -> Sequence[CapturedPacket]:
        return list(self.create_loader(reader))

    def dump(self, writer: BinaryIO, value: Sequence[CapturedPacket], **kwargs):
        dumper = self.create_dumper(writer, **kwargs)
        dumper.dump_header()
        for captured_packet in value:
            dumper.dump_packet(captured_packet)
