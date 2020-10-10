"""
    pyexcel_odsr.odsr
    ~~~~~~~~~~~~~~~~~~~
    The lower level ods file format handler using messytables

    :copyright: (c) 2015-2020 by Onni Software Ltd & its contributors
    :license: New BSD License
"""
from io import BytesIO

import pyexcel_io.service as service
from pyexcel_io.plugin_api.abstract_reader import IReader
from pyexcel_io.plugin_api.abstract_sheet import ISheet

from pyexcel_odsr.messyods import FODSTableSet, ODSTableSet


class ODSSheet(ISheet):
    """native ods sheet"""

    def __init__(
        self,
        sheet,
        auto_detect_int=True,
        auto_detect_float=True,
        auto_detect_datetime=True,
        **keywords
    ):
        self._native_sheet = sheet
        self._keywords = keywords
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
        if cell[1] in service.VALUE_CONVERTERS:
            n_value = service.VALUE_CONVERTERS[cell[1]](cell[0])
            if cell[1] == "float" and self.__auto_detect_int:
                if service.has_no_digits_in_float(n_value):
                    n_value = int(n_value)
            ret = n_value
        else:
            ret = cell[0]
        return ret


class ODSBook(IReader):
    """read ods book"""

    def __init__(self, file_alike_object, file_type, **keywords):
        self._native_book = self.get_native_book(file_alike_object)
        self._keywords = keywords
        tables = self._native_book.make_tables()
        self.content_array = [
            NameObject(table.name, table) for table in tables
        ]

    def read_sheet(self, sheet_index):
        """read a sheet at a specified index"""
        table = self.content_array[sheet_index].sheet
        sheet = ODSSheet(table, **self._keywords)
        return sheet

    def get_native_book(self, file_alike_object):
        return ODSTableSet(file_alike_object)

    def close(self):
        pass


class ODSBookInContent(ODSBook):
    def __init__(self, file_content, file_type, **keywords):
        file_stream = BytesIO(file_content)
        super().__init__(file_stream, file_type, **keywords)


class FODSBook(ODSBook):
    """read fods book"""

    def get_native_book(self, file_alike_object):
        return FODSTableSet(file_alike_object)


class FODSBookInConent(ODSBookInContent):
    """read fods book"""

    def get_native_book(self, file_alike_object):
        return FODSTableSet(file_alike_object)


class NameObject(object):
    def __init__(self, name, sheet):
        self.name = name
        self.sheet = sheet
