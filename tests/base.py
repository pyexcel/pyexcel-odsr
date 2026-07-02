import datetime  # noqa
import os  # noqa

import pyexcel
import pytest


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
        assert self.data["Sheet1"][0][0] == "Date"
        assert self.data["Sheet1"][1][0].strftime(date_format) == "11/11/2014"
        assert self.data["Sheet1"][2][0].strftime(date_format) == "01/01/2001"
        assert self.data["Sheet1"][3][0] == ""
        # time formats
        time_format = "%S:%M:%H"
        assert self.data["Sheet1"][0][1] == "Time"
        assert self.data["Sheet1"][1][1].strftime(time_format) == "12:12:11"
        assert self.data["Sheet1"][2][1].strftime(time_format) == "12:00:00"
        assert self.data["Sheet1"][3][1] == 0
        assert self.data["Sheet1"][4][1] == datetime.timedelta(
            hours=27, minutes=17, seconds=54
        )
        assert self.data["Sheet1"][5][1] == "Other"
        # boolean
        assert self.data["Sheet1"][0][2] == "Boolean"
        assert self.data["Sheet1"][1][2] is True
        assert self.data["Sheet1"][2][2] is False
        # Float
        assert self.data["Sheet1"][0][3] == "Float"
        assert self.data["Sheet1"][1][3] == 11.11
        # Currency
        assert self.data["Sheet1"][0][4] == "Currency"
        assert self.data["Sheet1"][1][4] == "1 GBP"
        assert self.data["Sheet1"][2][4] == "-10000 GBP"
        # Percentage
        assert self.data["Sheet1"][0][5] == "Percentage"
        assert self.data["Sheet1"][1][5] == 2
        # int
        assert self.data["Sheet1"][0][6] == "Int"
        assert self.data["Sheet1"][1][6] == 3
        assert self.data["Sheet1"][4][6] == 11
        # Scientifed not supported
        assert self.data["Sheet1"][1][7] == 100000
        # Fraction
        assert self.data["Sheet1"][1][8] == 1.25
        # Text
        assert self.data["Sheet1"][1][9] == "abc"

    def test_no_excessive_trailing_columns(self):
        with pytest.raises(IndexError):
            _ = self.data["Sheet1"][2][6]
