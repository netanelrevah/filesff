from gzip import GzipFile
from tempfile import NamedTemporaryFile

from filesff.accessors.csvs import csv_file_dicts_accessor, csv_file_lists_accessor
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


def test_load_rows_as_dicts_from_csv_file(tmp_path):
    csv_file_path = tmp_path / "test.csv"
    csv_file_path.write_text("a,b,c\n1,2,3\n4,5,6\n")

    csv_file_accessor = csv_file_dicts_accessor(csv_file_path)

    rows = []
    with csv_file_accessor.create_loader() as loader:
        assert loader.fields_names == ["a", "b", "c"]
        for row in loader:
            rows.append(row)
    assert rows == [
        {"a": "1", "b": "2", "c": "3"},
        {"a": "4", "b": "5", "c": "6"},
    ]


def test_load_rows_as_lists_from_csv_file(tmp_path):
    csv_file_path = tmp_path / "test.csv"
    csv_file_path.write_text("a,b,c\n1,2,3\n4,5,6\n")

    csv_file_accessor = csv_file_lists_accessor(csv_file_path)

    rows = []
    with csv_file_accessor.create_loader() as loader:
        assert loader.fields_names == ["a", "b", "c"]
        for row in loader:
            rows.append(row)
    assert rows == [
        ["1", "2", "3"],
        ["4", "5", "6"],
    ]


def test_dump_dicts_as_rows_into_csv_file(tmp_path):
    csv_file_path = tmp_path / "test.csv"

    csv_file_accessor = csv_file_dicts_accessor(csv_file_path)

    rows = [
        {"a": "1", "b": "2", "c": "3"},
        {"a": "4", "b": "5", "c": "6"},
    ]
    with csv_file_accessor.create_dumper(fields_names=["a", "b", "c"]) as dumper:
        dumper.dump_header()
        for row in rows:
            dumper.dump_row(row)

    assert csv_file_path.read_text() == "a,b,c\n1,2,3\n4,5,6\n"


def test_dump_lists_as_rows_into_csv_file(tmp_path):
    csv_file_path = tmp_path / "test.csv"

    csv_file_accessor = csv_file_lists_accessor(csv_file_path)

    rows = [
        ["1", "2", "3"],
        ["4", "5", "6"],
    ]
    with csv_file_accessor.create_dumper(fields_names=["a", "b", "c"]) as dumper:
        dumper.dump_header()
        for row in rows:
            dumper.dump_row(row)

    assert csv_file_path.read_text() == "a,b,c\n1,2,3\n4,5,6\n"
