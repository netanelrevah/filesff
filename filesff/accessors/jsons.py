from filesff.core.accessors import FileAccessor, LinesFileAccessor
from filesff.core.handlers import FileHandle
from filesff.formatters.jsons import JsonFormatter


def json_file(file_path, file_handle_cls=FileHandle, indentation=2):
    return FileAccessor.of(
        file_path=file_path,
        formatter=JsonFormatter(indentation=indentation),
        file_handle_cls=file_handle_cls,
    )


def json_lines_file(file_path, file_handle_cls=FileHandle):
    return LinesFileAccessor.of(
        file_path=file_path,
        formatter=JsonFormatter(indentation=0),
        file_handle_cls=file_handle_cls,
    )
