import sys
import math

from pyexcel_io.book import BookReader
from pyexcel_io.sheet import SheetReader

from pyexcel_odsr.messyods import ODSTableSet
import pyexcel_odsr.converter as converter

PY2 = sys.version_info[0] == 2

PY27_BELOW = PY2 and sys.version_info[1] < 7
if PY27_BELOW:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict


class ODSSheet(SheetReader):
    """native ods sheet"""
    def __init__(self, sheet, auto_detect_int=True,
                 auto_detect_float=True,
                 auto_detect_datetime=True,
                 **keywords):
        SheetReader.__init__(self, sheet, **keywords)
        self.__auto_detect_int = auto_detect_int
        self.__auto_detect_float = auto_detect_float
        self.__auto_detect_datetime = auto_detect_datetime

    @property
    def name(self):
        return self._native_sheet.name

    def row_iterator(self):
        return self._native_sheet.raw()

    def column_iterator(self, row):
        for cell in row:
            yield self.__convert_cell(cell)

    def __convert_cell(self, cell):
        ret = None
        if cell[1] in converter.VALUE_CONVERTERS:
            n_value = converter.VALUE_CONVERTERS[cell[1]](cell[0])
            if cell[1] == 'float' and self.__auto_detect_int:
                if is_integer_ok_for_xl_float(n_value):
                    n_value = int(n_value)
            ret = n_value
        else:
            ret = cell[0]
        return ret


class ODSBook(BookReader):
    """read ods book"""

    def open(self, file_name, **keywords):
        """open ods file"""
        BookReader.open(self, file_name, **keywords)
        self._load_from_file()

    def open_stream(self, file_stream, **keywords):
        """open ods file stream"""
        BookReader.open_stream(self, file_stream, **keywords)
        self._load_from_memory()

    def read_sheet_by_name(self, sheet_name):
        """read a named sheet"""
        tables = self._native_book.make_tables()
        rets = [table for table in tables
                if table.name == sheet_name]
        if len(rets) == 0:
            raise ValueError("%s cannot be found" % sheet_name)
        else:
            return self.read_sheet(rets[0])

    def read_sheet_by_index(self, sheet_index):
        """read a sheet at a specified index"""
        tables = self._native_book.make_tables()
        length = len(tables)
        if sheet_index < length:
            return self.read_sheet(tables[sheet_index])
        else:
            raise IndexError("Index %d of out bound %d" % (
                sheet_index, length))

    def read_all(self):
        """read all sheets"""
        result = OrderedDict()
        for sheet in self._native_book.make_tables():
            ods_sheet = ODSSheet(sheet, **self._keywords)
            result[ods_sheet.name] = ods_sheet.to_array()

        return result

    def read_sheet(self, native_sheet):
        """read one native sheet"""
        sheet = ODSSheet(native_sheet, **self._keywords)
        return {sheet.name: sheet.to_array()}

    def _load_from_memory(self):
        self._native_book = ODSTableSet(self._file_stream)

    def _load_from_file(self):
        self._native_book = ODSTableSet(self._file_name)


def is_integer_ok_for_xl_float(value):
    """check if a float had zero value in digits"""
    return value == math.floor(value)


_ods_registry = {
    "file_type": "ods",
    "reader": ODSBook,
    "stream_type": "binary",
    "mime_type": "application/vnd.oasis.opendocument.spreadsheet",
    "library": "pyexcel-odsr"
}

exports = (_ods_registry,)
