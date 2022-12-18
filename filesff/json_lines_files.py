import json

from filesff.formatted_files import FileAccessor


class JsonLinesFile(FileAccessor):
    LINES_FORMATTER = json

    def __iter__(self):
        for line in self.get_reader():
            yield self.LINES_FORMATTER.loads(line)
