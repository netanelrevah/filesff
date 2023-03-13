from io import BytesIO

import msgpack
from tstcls import TestClassBase

from filesff.msgpacks import MsgPackFileFormatter


class TestMsgPackFileFormatter(TestClassBase):
    def setup_test(self, **fixtures):
        self.tester = MsgPackFileFormatter()

    def test_load(self):
        reader = BytesIO(msgpack.dumps({}))

        ###
        assert {} == self.tester.load(reader)
        ###

    def test_dump(self):
        writer = BytesIO()

        ###
        self.tester.dump(writer, {})
        ###

        assert writer.getvalue() == msgpack.dumps({})
