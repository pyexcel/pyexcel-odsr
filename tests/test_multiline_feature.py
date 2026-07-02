import os

import pyexcel


def test_reading_multiline_ods():
    testfile = os.path.join("tests", "fixtures", "multilineods.ods")
    sheet = pyexcel.get_sheet(file_name=testfile, library="pyexcel-odsr")
    assert sheet[0, 0] == "1\n2\n3\n4"
    assert sheet[1, 0] == "Line 1\n\nLine 2"
