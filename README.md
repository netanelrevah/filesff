from filesff.protobuf_files import ProtoJsonFilefrom filesff.files_handlers import GzippedFileHandle# FilesFF - Files For Fun

a package that helps work with files with three level of abstraction:
* FilePointer - a pointer to a file (mostly path)
* FileHandle - a handle to the file to allow creating readers and writers to the
file in any encoding/compressing method
* FileAccessor - an accessor to the file to allow reading the formatted content
of the file as a python object and also to save python objects in the file format

for example, we want to read a json from gzip compressed file:

```python
from filesff.file_pointers import SimpleFilePointer
from filesff.files_handlers import GzippedFileHandle
from filesff.json_files import JsonFileAccessor

# the long way
pointer = SimpleFilePointer.of("/path/to/file.json")
handle = GzippedFileHandle(pointer)
accessor = JsonFileAccessor(handle)

json_data = accessor.load()

# or shorter
accessor = JsonFileAccessor.of("/path/to/file.json", GzippedFileHandle)

accessor.dump({"json": "data"})
```

another example, we want to write a protobuf into a temp file
```shell
pip install fileff[protobuf]
```

```python
from filesff.file_pointers import TemporaryFilePointer
from filesff.files_handlers import FileHandle
from filesff.protobuf_files import ProtoJsonFile

from messages.v1.messages_pb2 import Message

# the long way
pointer = TemporaryFilePointer.create()
handle = FileHandle(pointer)
accessor = ProtoJsonFile(handle, message_cls=Message)

message = accessor.load()

# or shorter
accessor = ProtoJsonFile.of_temp(message_cls=Message)

message = accessor.load()
```
