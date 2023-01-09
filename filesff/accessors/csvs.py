from filesff.core.accessors import ContinuousFileAccessor
from filesff.core.handlers import FileHandle
from filesff.formatters.csvs import CsvDictFormatter


def csv_dicts_file(file_path, file_handle_cls=FileHandle):
    return ContinuousFileAccessor.of(
        file_path=file_path,
        formatter=CsvDictFormatter(),
        file_handle_cls=file_handle_cls,
    )


def csv_dicts_temp_file(file_handle_cls=FileHandle):
    return ContinuousFileAccessor.of_temp(
        formatter=CsvDictFormatter(),
        file_handle_cls=file_handle_cls,
    )
