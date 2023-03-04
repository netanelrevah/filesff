from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp

from filesff.gzips import GzippedFileHandle
from filesff.jsons import JsonFormatter
from filesff.paths import PathFileHandle
from filesff.protobufs import ProtoBytesFileFormatter

accessor = GzippedFileHandle.of_str("./file.gz").access(JsonFormatter())
accessor.dump({"json": "data"})

accessor = PathFileHandle.of_temp().access(ProtoBytesFileFormatter)
now = Timestamp()
now.FromDatetime(datetime.now())
accessor.dump(now)

loaded_now = accessor.load(message_cls=Timestamp)
