# FilesFF - Files For Fun

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
from filesff.core.handlers import GzippedFileHandle
from filesff.accessors.jsons import json_file_accessor

accessor = json_file_accessor("/path/to/file.gz", GzippedFileHandle)

accessor.dump({"json": "data"})
```

write a protobuf into a temp file
```shell
pip install fileff[protobuf]
```

```python
from filesff.accessors.protobufs import temp_protobuf_file_accessor

from messages.v1.messages_pb2 import Message

accessor = temp_protobuf_file_accessor(message_cls=Message)

message = accessor.load()
```

implement new file format:

```python
from filesff.core.formatters import FileFormatter

class NewFileFormatter(FileFormatter):
    def load(self, reader: IO) -> AnyStr:
        return reader.read().replace("a", "e")

    def dump(self, writer: IO, value: Any):
        writer.write(value.replace("e", "a"))
```

use it 
```python
from filesff.core.accessors import FileAccessor

file_accessor = FileAccessor.of("/a/file/path.ae", NewFileFormatter())
file_accessor.load()
```


