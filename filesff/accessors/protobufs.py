from filesff.core.accessors import FileAccessor
from filesff.core.handlers import FileHandle
from filesff.formatters.protobufs import ProtoBytesFileFormatter, ProtoJsonFileFormatter


def protobuf_file(file_path, message_cls, file_handle_cls=FileHandle):
    return FileAccessor.of(
        file_path,
        ProtoBytesFileFormatter(message_cls),
        file_handle_cls,
    )


def protojson_file(file_path, message_cls, file_handle_cls=FileHandle):
    return FileAccessor.of(
        file_path,
        ProtoJsonFileFormatter(message_cls),
        file_handle_cls,
    )
