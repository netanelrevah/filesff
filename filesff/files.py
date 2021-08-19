import errno
import os
import tempfile
from gzip import GzipFile


class FilePointerInterface(object):
    """
    Simple interface to point onto file
    """
    @property
    def file_path(self):
        raise NotImplementedError()


class FilePointer(FilePointerInterface):
    """
    Default implementation to point onto file with string path
    """
    def __init__(self, file_path):
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path


class TemporaryFilePointer(FilePointerInterface):
    """
    file pointer to temp file, the temp file will be removed when there will be no references
    """
    def __init__(self, delete=True, prefix='', suffix='', file_extension='', directory=None):
        """
        :param delete: should we delete the file when there will be no references?
        :param prefix: prefix of the file name
        :param suffix: suffix of the file name (for extension use file_extension)
        :param file_extension: file extension (after the '.')
        :param directory: directory to create the temp file into
        """
        self.delete = delete

        # we created file with the default interface and remove it immediately because we need only path
        self._file_path = tempfile.NamedTemporaryFile(
            delete=True,  # don't be confuse with the self.delete because here we need only the path!
            prefix=prefix,
            suffix=suffix + file_extension,
            dir=directory,
        ).name

    @property
    def file_path(self):
        return self._file_path

    def __del__(self):
        if not self.delete:
            return

        try:
            os.remove(self.file_path)
        except OSError:
            pass


class FileHandle(object):
    """
    basic handle to regular file to use for creating writers and readers according the file type
    """
    FILE_NAME_EXTENSION = ''
    FILE_NAME_ADDITIONAL_EXTENSIONS = []
    COMPRESSED = False

    def __init__(self, pointer: FilePointerInterface) -> None:
        self.pointer = pointer

    @property
    def file_path(self):
        return self.pointer.file_path

    @property
    def extension(self):
        return self.FILE_NAME_EXTENSION

    @property
    def is_compressed(self):
        return self.COMPRESSED

    @property
    def file_size(self):
        return os.stat(self.file_path).st_size

    def create_empty_file(self):
        """
        initialize empty file in the path of the pointer if the file not exists
        """
        if not os.path.exists(self.file_path):
            self.create_writer()

    def create_writer(self, write_mode='wb'):
        return open(self.file_path, mode=write_mode)

    def create_reader(self):
        self.create_empty_file()   # we must have at least empty file to create reader
        return open(self.file_path, mode='rb')

    @classmethod
    def new_temporary_file(cls, delete=True, prefix='', suffix='', directory=None):
        """
        use this method to create file handle for temp file
        """
        return cls(TemporaryFilePointer(
            delete=delete,
            prefix=prefix,
            suffix=suffix,
            file_extension=cls.FILE_NAME_EXTENSION,
            directory=directory
        ))

    @classmethod
    def from_file_path(cls, file_path):
        """
        convenience way to open simple file path
        """
        return cls(FilePointer(file_path))


class GzippedFileHandle(FileHandle):
    FILE_NAME_EXTENSION = '.gz'
    FILE_NAME_ADDITIONAL_EXTENSIONS = ['.gzip']
    COMPRESSED = True

    def create_writer(self, write_mode='wb'):
        return GzipFile(fileobj=super(GzippedFileHandle, self).create_writer(write_mode=write_mode))

    def create_reader(self):
        return GzipFile(fileobj=super(GzippedFileHandle, self).create_reader())


def create_directory_if_absence(file_path):
    """
    python2.7 doesn't have exist_ok option so this supplies the same logic
    """
    dir_name = os.path.dirname(file_path)

    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
