from dataclasses import dataclass
from typing import IO, Any, AnyStr

from filesff.core.formatters import FileFormatter, StringFormatter

try:
    import ujson as json
except ImportError:
    import json


@dataclass
class JsonFormatter(FileFormatter, StringFormatter):
    indentation: int

    def load(self, reader: IO) -> AnyStr:
        return json.load(fp=reader)

    def dump(self, writer: IO, value: Any):
        json.dump(obj=value, fp=writer, indent=self.indentation)

    def loads(self, formatted_value: AnyStr) -> Any:
        return json.loads(s=formatted_value)

    def dumps(self, value: Any) -> AnyStr:
        return json.dumps(obj=value, indent=self.indentation)
