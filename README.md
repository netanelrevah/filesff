# FilesFF - Files For Fun

a package that helps work with files with three level of abstraction:
* FilePointer - a pointer to a file (mostly path)
* FileHandle - a handle to the file to allow creating readers and writers to the
file in any encoding/compressing method
* FileAccessor - an accessor to the file to allow reading the formatted content
of the file as a python object and also to save python objects in the file format

for example, we want to read a json from gzip compressed file:

```python
from filesff.core.handlers import GzippedFileHandle
from filesff.accessors.jsons import json_file

accessor = json_file("/path/to/file.gz", GzippedFileHandle)

accessor.dump({"json": "data"})
```

another example, we want to write a protobuf into a temp file
```shell
pip install fileff[protobuf]
```

```python
from filesff.accessors.protobufs import protobuf_temp_file

from messages.v1.messages_pb2 import Message

accessor = protobuf_temp_file(message_cls=Message)

message = accessor.load()
```
