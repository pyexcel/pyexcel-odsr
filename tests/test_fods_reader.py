import os

from base import ODSCellTypes
from pyexcel_io.reader import Reader

from pyexcel_odsr.odsr import FODSBook


class TestFODSReader(ODSCellTypes):
    def setUp(self):
        r = Reader("fods")
        r.reader_class = FODSBook
        r.open(os.path.join("tests", "fixtures", "ods_formats.fods"))
        self.data = r.read_all()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])
        r.close()


class TestFODSReaderStream(ODSCellTypes):
    def setUp(self):
        with open(
            os.path.join("tests", "fixtures", "ods_formats.fods"), "rb"
        ) as f:
            r = Reader("fods")
            r.reader_class = FODSBook
            r.open_stream(f)
            self.data = r.read_all()
            for key in self.data.keys():
                self.data[key] = list(self.data[key])
            r.close()
