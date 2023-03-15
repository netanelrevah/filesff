import json
from io import StringIO

from tstcls import TestClassBase

from filesff.jsons import JsonFormatter, JsonLinesFileDumper, JsonLinesFileLoader


class TestJsonFormatter(TestClassBase):
    def setup_test(self, **fixtures):
        self.tester = JsonFormatter()

    def test_load(self):
        reader = StringIO(json.dumps({}))

        ###
        assert {} == self.tester.load(reader)
        ###

    def test_dump(self):
        writer = StringIO()

        ###
        self.tester.dump(writer, {})
        ###

        assert writer.getvalue() == "{}"


class TestJsonLinesFileLoader(TestClassBase):
    def setup_test(self, **fixtures):
        self.reader = StringIO()
        self.tester = JsonLinesFileLoader(self.reader)

    def test_iter(self):
        self.reader.write("{}\n[]")
        self.reader.seek(0)

        ###
        assert list(self.tester) == [{}, []]
        ###


class TestJsonLinesFileDumper(TestClassBase):
    def setup_test(self, **fixtures):
        self.writer = StringIO()
        self.tester = JsonLinesFileDumper(self.writer)

    def test_dump_object(self):
        ###
        self.tester.dump_object([])
        self.tester.dump_object({})
        ###

        assert self.writer.getvalue() == "[]\n{}"
