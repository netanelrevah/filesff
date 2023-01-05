from gzip import GzipFile
from tempfile import NamedTemporaryFile

from filesff.file_pointers import TemporaryFilePointer
from filesff.files_handlers import GzippedFileHandle


def test_context_manager_temp_file():
    with TemporaryFilePointer.create() as tfp:
        file_path = tfp.path
        assert not tfp.exists()
        file_path.write_text("d")
        assert tfp.exists()
    assert not file_path.exists()

    del tfp
    assert not file_path.exists()


def test_regular_temp_file():
    tfp = TemporaryFilePointer.create()
    file_path = tfp.path
    assert not tfp.exists()
    file_path.write_text("d")
    assert tfp.exists()
    del tfp
    assert not file_path.exists()


def test_gzip_file():
    temp_file_path = NamedTemporaryFile(delete=True).name

    gzip_file = GzipFile(filename=temp_file_path, mode="w")
    gzip_file.write(b"blablabla")
    gzip_file.close()

    handle = GzippedFileHandle.of(temp_file_path)
    assert handle.create_text_reader().read() == "blablabla"
    assert handle.create_bytes_reader().read() == b"blablabla"

    assert handle.create_compressed_reader() != b"blablabla"
    assert handle.create_compressed_reader() != "blablabla"
