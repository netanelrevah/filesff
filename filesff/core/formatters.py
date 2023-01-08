from typing import IO, Any, AnyStr


class StringFormatter:
    def loads(self, formatted_value: AnyStr) -> Any:
        raise NotImplementedError()

    def dumps(self, value: Any) -> AnyStr:
        raise NotImplementedError()


class FileFormatter:
    def load(self, reader: IO) -> AnyStr:
        raise NotImplementedError()

    def dump(self, writer: IO, value: Any):
        raise NotImplementedError()
