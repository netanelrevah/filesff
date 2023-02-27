# FilesFF - Files For Fun

[![PyPI version](https://img.shields.io/pypi/v/fileff.svg)](https://pypi.python.org/pypi/filesff/) [![PyPI downloads](https://img.shields.io/pypi/dm/filesff.svg)](https://pypi.python.org/pypi/filesff/)

* python package to work with file handles
* use handles of files as parameters without keeping open files
* replace file handles easily with mocks
* handle many file types with generic protocol

to install

```shell
pip install filesff
```

## Usage

read a json from gzip compressed file:

```python
accessor = json_file_accessor("./file.gz", GzippedFileHandle)
accessor.dump({"json": "data"})
```

write a protobuf into a temp file
```shell
pip install fileff[protobuf]
```

```python
from google.protobuf.timestamp_pb2 import Timestamp

accessor = temp_protobuf_file_accessor()
now = Timestamp()
now.FromDatetime(datetime.now())
accessor.dump(now)

loaded_now = accessor.load(message_cls=Timestamp)
```

implement new file format:

```python
class NewFileFormatter(FullTextFileFormatter):
    def load(self, reader: TextIO, **_) -> AnyStr:
        return reader.read().replace("a", "e")

    def dump(self, writer: TextIO, value: Any, **_):
        writer.write(value.replace("e", "a"))
```

use it 
```python
file_accessor = FullFileAccessor.of("./path.ae", NewFileFormatter())
file_accessor.dump("ababab")
```


