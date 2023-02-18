from filesff.core.accessors import FileAccessor, FullFileAccessor
from filesff.core.handlers import FileHandle
from filesff.formatters.protobufs import (
    ProtoBytesFileFormatter,
    ProtoJsonFileFormatter,
    ProtoJsonLinesFileFormatter,
)


def protobuf_file_accessor(file_path, file_handle_cls=FileHandle):
    return FullFileAccessor.of(
        file_path,
        ProtoBytesFileFormatter(),
        file_handle_cls,
    )


def temp_protobuf_file_accessor(file_handle_cls=FileHandle):
    return FullFileAccessor.of_temp(
        ProtoBytesFileFormatter(),
        file_handle_cls,
    )


def protojson_file_accessor(file_path, file_handle_cls=FileHandle):
    return FullFileAccessor.of(
        file_path,
        ProtoJsonFileFormatter(),
        file_handle_cls,
    )


def temp_protojson_file_accessor(file_handle_cls=FileHandle):
    return FullFileAccessor.of_temp(
        ProtoJsonFileFormatter(),
        file_handle_cls,
    )


def protojson_lines_file_accessor(file_path, file_handle_cls=FileHandle):
    return FileAccessor.of(
        file_path,
        ProtoJsonLinesFileFormatter(),
        file_handle_cls,
    )


def temp_protojson_lines_file_accessor(file_handle_cls=FileHandle):
    return FileAccessor.of_temp(
        ProtoJsonLinesFileFormatter(),
        file_handle_cls,
    )
