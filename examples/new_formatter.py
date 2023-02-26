from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp

from filesff.jsons import json_file_accessor
from filesff.protobufs import temp_protobuf_file_accessor
from filesff.core.handlers import GzippedFileHandle

accessor = json_file_accessor("./file.gz", GzippedFileHandle)
accessor.dump({"json": "data"})

accessor = temp_protobuf_file_accessor()
now = Timestamp()
now.FromDatetime(datetime.now())
accessor.dump(now)

loaded_now = accessor.load(message_cls=Timestamp)
