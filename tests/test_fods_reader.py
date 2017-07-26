import os
from pyexcel_odsr.odsr import FODSBook

from base import ODSCellTypes


class TestFODSReader(ODSCellTypes):
    def setUp(self):
        r = FODSBook()
        r.open(os.path.join("tests",
                            "fixtures",
                            "ods_formats.fods"))
        self.data = r.read_all()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])
        r.close()


class TestFODSReaderStream(ODSCellTypes):
    def setUp(self):
        with open(os.path.join("tests",
                               "fixtures",
                               "ods_formats.fods"), 'rb') as f:
            r = FODSBook()
            r.open_stream(f)
            self.data = r.read_all()
            for key in self.data.keys():
                self.data[key] = list(self.data[key])
            r.close()
