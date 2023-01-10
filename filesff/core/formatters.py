from typing import IO, Any, AnyStr, Generator


class FileFormatter:
    def load(self, reader: IO) -> AnyStr:
        raise NotImplementedError()

    def dump(self, writer: IO, value: Any):
        raise NotImplementedError()


class ContinuesFileFormatter:
    def load_continuously(self, reader: IO) -> Generator[AnyStr, None, None]:
        raise NotImplementedError()

    def dump_continuously(self, writer: IO) -> Generator[None, Any, None]:
        raise NotImplementedError()
