# FilesFF - Files For Fun

[![PyPI version](https://img.shields.io/pypi/v/filesff.svg)](https://pypi.python.org/pypi/filesff/) [![PyPI downloads](https://img.shields.io/pypi/dm/filesff.svg)](https://pypi.python.org/pypi/filesff/)![GitHub](https://img.shields.io/github/license/netanelrevah/filesff)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/filesff)

* python package to work with file handles
* use handles of files as parameters without keeping open files
* replace file handles easily with mocks
* handle many file types with generic protocol

to install with all extras

```shell
pip install filesff[protobug,ujson,cap,msgpack,s3]
```

## Usage

read a json from gzip compressed file:

```python
accessor = GzippedFileHandle.of_str("./file.gz").access(JsonFormatter())
accessor.dump({"json": "data"})
```

write a protobuf into a temp file
```shell
pip install fileff[protobuf]
```

```python
from google.protobuf.timestamp_pb2 import Timestamp

accessor = PathFileHandle.of_temp().access(ProtoBytesFileFormatter)
now = Timestamp()
now.FromDatetime(datetime.now())
accessor.dump(now)

loaded_now = accessor.load(message_cls=Timestamp)
```

implement new file format:

```python
class NewFileFormatter(FullTextFileFormatter):
    def load(self, reader: IO, **_) -> AnyStr:
        return reader.read().replace("a", "e")

    def dump(self, writer: IO, value: Any, **_):
        writer.write(value.replace("e", "a"))
```

use it 
```python
file_accessor = PathFileHandle.of_str("./path.ae").access(NewFileFormatter())
file_accessor.dump("ababab")
```


