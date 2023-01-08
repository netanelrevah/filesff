from gzip import GzipFile
from tempfile import NamedTemporaryFile

from filesff.core.handlers import GzippedFileHandle
from filesff.core.pointers import TemporaryFilePointer


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

    with GzipFile(filename=temp_file_path, mode="w") as gzip_file:
        gzip_file.write(b"blablabla")

    handle = GzippedFileHandle.of(temp_file_path)

    with handle.create_text_reader() as reader:
        assert reader.read() == "blablabla"

    with handle.create_bytes_reader() as reader:
        assert reader.read() == b"blablabla"

    with handle.create_compressed_reader() as reader:
        value = reader.read()
        assert value != b"blablabla" and value != "blablabla"
