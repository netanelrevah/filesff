from filesff.files import TemporaryFilePointer


def test_context_manager_temp_file():
    with TemporaryFilePointer.create() as tfp:
        file_path = tfp.file_path
        assert not tfp.file_path.exists()
        file_path.write_text("d")
        assert tfp.file_path.exists()
    assert not file_path.exists()

    del tfp
    assert not file_path.exists()


def test_regular_temp_file():
    tfp = TemporaryFilePointer.create()
    file_path = tfp.file_path
    assert not tfp.file_path.exists()
    file_path.write_text("d")
    assert tfp.file_path.exists()
    del tfp
    assert not file_path.exists()
