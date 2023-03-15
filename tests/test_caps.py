from datetime import datetime
from io import BytesIO

import cap
from cap import CapturedPacket
from tstcls import TestClassBase

from filesff.caps import CapFileFormatter


class TestCapFileFormatter(TestClassBase):
    def setup_test(self, **fixtures):
        self.tester = CapFileFormatter()

    def test_load(self):
        captured_packets = [
            CapturedPacket.from_datetime(b"abcd", datetime.now()),
            CapturedPacket.from_datetime(b"abcdef", datetime.now()),
        ]

        reader = BytesIO(cap.dumps(captured_packets))

        ###
        assert captured_packets == self.tester.load(reader)
        ###

    def test_dump(self):
        captured_packets = [
            CapturedPacket.from_datetime(b"abcd", datetime.now()),
            CapturedPacket.from_datetime(b"abcdef", datetime.now()),
        ]
        writer = BytesIO()

        ###
        self.tester.dump(writer, captured_packets)
        ###

        assert writer.getvalue() == cap.dumps(captured_packets)
