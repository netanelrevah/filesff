from typing import IO, Any, AnyStr

from filesff.core.accessors import FullFileAccessor
from filesff.core.formatters import FullFileFormatter


class NewFileFormatter(FullFileFormatter):
    def load(self, reader: IO, **_) -> AnyStr:
        return reader.read().replace("a", "e")

    def dump(self, writer: IO, value: Any, **_):
        writer.write(value.replace("e", "a"))


file_accessor = FullFileAccessor.of("./path.ae", NewFileFormatter())
file_accessor.dump("ababab")
