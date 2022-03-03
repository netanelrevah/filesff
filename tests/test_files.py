import tempfile
from pathlib import Path

from tstcls import TestClassBase

from filesff.files import FileHandle, FilePointer, TemporaryFilePointer


def test_file_pointer():
    temp_file_path = tempfile.NamedTemporaryFile()

    ###
    file_pointer = FilePointer(temp_file_path.name)
    ###

    assert file_pointer.file_path == Path(temp_file_path.name)
    assert file_pointer.file_path_str == temp_file_path.name


def test_temporary_file_pointer():
    temp_directory = tempfile.TemporaryDirectory()
    temp_directory_path = Path(temp_directory.name)

    ###
    file_pointer = TemporaryFilePointer(directory=temp_directory_path)
    ###

    assert not file_pointer.file_path.exists()
    assert list(temp_directory_path.glob("*")) == []


class TestFileHandle(TestClassBase):
    def setup_test(self):
        self.pointer = TemporaryFilePointer()
        self.tester = FileHandle(self.pointer)

    def test_file_size(self):
        content = "Content"
        open(self.pointer.file_path, "w").write(content)

        ###
        assert self.tester.file_size == len(content)
        ###
