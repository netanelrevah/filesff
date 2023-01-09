from filesff.core.accessors import ContinuousFileAccessor, FileAccessor
from filesff.core.handlers import FileHandle
from filesff.formatters.jsons import JsonFormatter, JsonLinesFormatter


def json_file(file_path, file_handle_cls=FileHandle, indentation=2):
    return FileAccessor.of(
        file_path=file_path,
        formatter=JsonFormatter(indentation=indentation),
        file_handle_cls=file_handle_cls,
    )


def json_temp_file(file_handle_cls=FileHandle, indentation=2):
    return FileAccessor.of_temp(
        formatter=JsonFormatter(indentation=indentation),
        file_handle_cls=file_handle_cls,
    )


def json_lines_file(file_path, file_handle_cls=FileHandle):
    return ContinuousFileAccessor.of(
        file_path=file_path,
        formatter=JsonLinesFormatter(),
        file_handle_cls=file_handle_cls,
    )


def json_lines_temp_file(file_handle_cls=FileHandle):
    return ContinuousFileAccessor.of_temp(
        formatter=JsonLinesFormatter(),
        file_handle_cls=file_handle_cls,
    )