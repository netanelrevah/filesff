from filesff.file_pointers import TemporaryFilePointer


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
