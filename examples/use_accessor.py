from typing import IO, Any, AnyStr

from filesff.core.formatters import FullTextFileFormatter
from filesff.paths import PathFileHandle


class NewFileFormatter(FullTextFileFormatter):
    def load(self, reader: IO, **_) -> AnyStr:
        return reader.read().replace("a", "e")

    def dump(self, writer: IO, value: Any, **_):
        writer.write(value.replace("e", "a"))


file_accessor = PathFileHandle.of_str("./path.ae").access(NewFileFormatter())
file_accessor.dump("ababab")
