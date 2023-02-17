from filesff.core.accessors import FileAccessor
from filesff.core.handlers import FileHandle
from filesff.formatters.csvs import CsvFileDictFormatter, CsvFileListsFormatter


def create_csv_file_dict_accessor(file_path, file_handle_cls=FileHandle):
    return FileAccessor.of(
        file_path=file_path,
        formatter=CsvFileDictFormatter(),
        file_handle_cls=file_handle_cls,
    )


def create_csv_temp_file_dict_accessor(file_handle_cls=FileHandle):
    return FileAccessor.of_temp(
        formatter=CsvFileDictFormatter(),
        file_handle_cls=file_handle_cls,
    )


def create_csv_file_lists_accessor(file_path, file_handle_cls=FileHandle):
    return FileAccessor.of(
        file_path=file_path,
        formatter=CsvFileListsFormatter(),
        file_handle_cls=file_handle_cls,
    )


def create_csv_temp_file_lists_accessor(file_path, file_handle_cls=FileHandle):
    return FileAccessor.of_temp(
        formatter=CsvFileListsFormatter(),
        file_handle_cls=file_handle_cls,
    )
