import os

from base import ODSCellTypes
from pyexcel._compact import BytesIO
from pyexcel_ods.odsw import ODSWriter

from pyexcel_odsr.odsr import ODSBook


class TestODSReader(ODSCellTypes):
    def setUp(self):
        r = ODSBook(
            os.path.join("tests", "fixtures", "ods_formats.ods"), "ods"
        )
        self.data = r.read_all()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])
        r.close()


class TestODSReaderStream(ODSCellTypes):
    def setUp(self):
        with open(
            os.path.join("tests", "fixtures", "ods_formats.ods"), "rb"
        ) as f:
            r = ODSBook(f, "ods")
            self.data = r.read_all()
            for key in self.data.keys():
                self.data[key] = list(self.data[key])
        r.close()


class TestODSReaderBytesIO(ODSCellTypes):
    def setUp(self):
        with open(
            os.path.join("tests", "fixtures", "ods_formats.ods"), "rb"
        ) as f:
            io = BytesIO(f.read())
            r = ODSBook(io, "ods")
            self.data = r.read_all()
            for key in self.data.keys():
                self.data[key] = list(self.data[key])
        r.close()


class TestODSWriter(ODSCellTypes):
    def setUp(self):
        r = ODSBook(
            os.path.join("tests", "fixtures", "ods_formats.ods"), "ods"
        )
        self.data1 = r.read_all()
        self.testfile = "odswriter.ods"
        w = ODSWriter(self.testfile, "ods")
        w.write(self.data1)
        w.close()
        r2 = ODSBook(self.testfile, "ods")
        self.data = r2.read_all()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
