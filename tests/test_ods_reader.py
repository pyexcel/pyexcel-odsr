import os

from base import ODSCellTypes
from pyexcel._compact import BytesIO
from pyexcel_io.reader import Reader
from pyexcel_io.writer import Writer
from pyexcel_ods.odsw import ODSWriter

from pyexcel_odsr.odsr import ODSBook


class TestODSReader(ODSCellTypes):
    def setUp(self):
        r = Reader("fods")
        r.reader_class = ODSBook
        r.open(os.path.join("tests", "fixtures", "ods_formats.ods"))
        self.data = r.read_all()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])
        r.close()


class TestODSReaderStream(ODSCellTypes):
    def setUp(self):
        with open(
            os.path.join("tests", "fixtures", "ods_formats.ods"), "rb"
        ) as f:
            r = Reader("fods")
            r.reader_class = ODSBook
            r.open_stream(f)
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
            r = Reader("fods")
            r.reader_class = ODSBook
            r.open_stream(io)
            self.data = r.read_all()
            for key in self.data.keys():
                self.data[key] = list(self.data[key])
        r.close()


class TestODSWriter(ODSCellTypes):
    def setUp(self):
        r = Reader("fods")
        r.reader_class = ODSBook
        r.open(os.path.join("tests", "fixtures", "ods_formats.ods"))
        self.data1 = r.read_all()
        r.close()
        self.testfile = "odswriter.ods"
        w = Writer("ods")
        w.writer_class = ODSWriter
        w.open(self.testfile)
        w.write(self.data1)
        w.close()
        r.open(self.testfile)
        self.data = r.read_all()
        for key in self.data.keys():
            self.data[key] = list(self.data[key])
        r.close()

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
