from dataclasses import dataclass
from typing import IO, Any, AnyStr, Generator

from filesff.core.formatters import ContinuesFileFormatter, FileFormatter

try:
    import ujson as json
except ImportError:
    import json


@dataclass
class JsonFormatter(FileFormatter):
    indentation: int

    def load(self, reader: IO) -> AnyStr:
        return json.load(fp=reader)

    def dump(self, writer: IO, value: Any):
        json.dump(obj=value, fp=writer, indent=self.indentation)


class JsonLinesFormatter(ContinuesFileFormatter):
    def load_continuously(self, reader: IO) -> Generator[AnyStr, None, None]:
        for line in reader:
            yield json.loads(line)

    def dump_continuously(self, writer: IO) -> Generator[None, dict, None]:
        while True:
            item = yield None
            writer.write(json.dumps(item, indent=0))
            writer.write("\n")
