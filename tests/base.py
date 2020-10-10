import datetime  # noqa
import os  # noqa

import pyexcel
from nose.tools import eq_, raises  # noqa


def create_sample_file1(file):
    data = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 1.1, 1]
    table = []
    table.append(data[:4])
    table.append(data[4:8])
    table.append(data[8:12])
    pyexcel.save_as(array=table, dest_file_name=file)


class ODSCellTypes:
    def test_formats(self):
        # date formats
        date_format = "%d/%m/%Y"
        eq_(self.data["Sheet1"][0][0], "Date")
        eq_(self.data["Sheet1"][1][0].strftime(date_format), "11/11/2014")
        eq_(self.data["Sheet1"][2][0].strftime(date_format), "01/01/2001")
        eq_(self.data["Sheet1"][3][0], "")
        # time formats
        time_format = "%S:%M:%H"
        eq_(self.data["Sheet1"][0][1], "Time")
        eq_(self.data["Sheet1"][1][1].strftime(time_format), "12:12:11")
        eq_(self.data["Sheet1"][2][1].strftime(time_format), "12:00:00")
        eq_(self.data["Sheet1"][3][1], 0)
        eq_(
            self.data["Sheet1"][4][1],
            datetime.timedelta(hours=27, minutes=17, seconds=54),
        )
        eq_(self.data["Sheet1"][5][1], "Other")
        # boolean
        eq_(self.data["Sheet1"][0][2], "Boolean")
        eq_(self.data["Sheet1"][1][2], True)
        eq_(self.data["Sheet1"][2][2], False)
        # Float
        eq_(self.data["Sheet1"][0][3], "Float")
        eq_(self.data["Sheet1"][1][3], 11.11)
        # Currency
        eq_(self.data["Sheet1"][0][4], "Currency")
        eq_(self.data["Sheet1"][1][4], "1 GBP")
        eq_(self.data["Sheet1"][2][4], "-10000 GBP")
        # Percentage
        eq_(self.data["Sheet1"][0][5], "Percentage")
        eq_(self.data["Sheet1"][1][5], 2)
        # int
        eq_(self.data["Sheet1"][0][6], "Int")
        eq_(self.data["Sheet1"][1][6], 3)
        eq_(self.data["Sheet1"][4][6], 11)
        # Scientifed not supported
        eq_(self.data["Sheet1"][1][7], 100000)
        # Fraction
        eq_(self.data["Sheet1"][1][8], 1.25)
        # Text
        eq_(self.data["Sheet1"][1][9], "abc")

        @raises(IndexError)
        def test_no_excessive_trailing_columns(self):
            eq_(self.data["Sheet1"][2][6], "")
