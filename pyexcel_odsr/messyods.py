"""
Copyright (c) 2012-2017 The Open Knowledge Foundation Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import io
import re
import sys
import zipfile

from lxml import etree
from pyexcel_io.service import VALUE_TOKEN

PY2 = sys.version_info[0] == 2

ODS_NAMESPACES_TAG_MATCH = re.compile(
    b"(<office:document-content[^>]*>)", re.MULTILINE
)
ODS_TABLE_MATCH = re.compile(
    rb".*?(<table:table.*?<\/.*?:table>).*?", re.MULTILINE
)
ODS_TABLE_NAME = re.compile(b'.*?table:name="(.*?)".*?')
ODS_ROW_MATCH = re.compile(
    rb".*?(<table:table-row.*?<\/.*?:table-row>).*?", re.MULTILINE
)
ODS_DOCUMENT_CLOSE_TAG = b"</office:document-content>"
FODS_NAMESPACES_TAG_MATCH = re.compile(b"(<office:document[^>]*>)", re.DOTALL)
FODS_TABLE_MATCH = re.compile(
    rb".*?(<table:table.*?<\/.*?:table>).*?", re.DOTALL
)
FODS_TABLE_NAME = re.compile(b'.*?table:name="(.*?)".*?')
FODS_ROW_MATCH = re.compile(
    rb".*?(<table:table-row.*?<\/.*?:table-row>).*?", re.DOTALL
)
FODS_DOCUMENT_CLOSE_TAG = b"</office:document>"
NS_OPENDOCUMENT_PTTN = u"urn:oasis:names:tc:opendocument:xmlns:%s"
NS_CAL_PTTN = u"urn:org:documentfoundation:names:experimental:calc:xmlns:%s"
NS_OPENDOCUMENT_TABLE = NS_OPENDOCUMENT_PTTN % "table:1.0"
NS_OPENDOCUMENT_OFFICE = NS_OPENDOCUMENT_PTTN % "office:1.0"

TABLE_CELL = "table-cell"
VALUE_TYPE = "value-type"
COLUMN_REPEAT = "number-columns-repeated"

DEFAULT_NAMESPACES = {
    "dc": u"http://purl.org/dc/elements/1.1/",
    "draw": NS_OPENDOCUMENT_PTTN % u"drawing:1.0",
    "number": NS_OPENDOCUMENT_PTTN % u"datastyle:1.0",
    "office": NS_OPENDOCUMENT_PTTN % u"office:1.0",
    "svg": NS_OPENDOCUMENT_PTTN % u"svg-compatible:1.0",
    "table": NS_OPENDOCUMENT_PTTN % u"table:1.0",
    "text": NS_OPENDOCUMENT_PTTN % u"text:1.0",
    "calcext": NS_CAL_PTTN % u"calcext:1.0",
}


class ODSTableSet(object):
    """
    A wrapper around ODS files. Because they are zipped and the info we want
    is in the zipped file as content.xml we must ensure that we either have
    a seekable object (local file) or that we retrieve all of the content from
    the remote URL.
    """

    def __init__(self, fileobj, window=None, **kw):
        """Initialize the object.

        :param fileobj: may be a file path or a file-like object. Note the
        file-like object *must* be in binary mode and must be seekable (it will
        get passed to zipfile).

        As a specific tip: urllib2.urlopen returns a file-like object that is
        not in file-like mode while urllib.urlopen *does*!

        To get a seekable file you *cannot* use
        messytables.core.seekable_stream as it does not support the full seek
        functionality.
        """
        if hasattr(fileobj, "read"):
            # wrap in a StringIO so we do not have hassle with seeks and
            # binary etc (see notes to __init__ above)
            # TODO: rather wasteful if in fact fileobj comes from disk
            fileobj = io.BytesIO(fileobj.read())

        self.window = window

        zf = zipfile.ZipFile(fileobj).open("content.xml")
        self.content = zf.read()
        zf.close()
        self._table_matcher = ODS_TABLE_MATCH
        self._document_close_tag = ODS_DOCUMENT_CLOSE_TAG
        self._namespace_tag_matcher = ODS_NAMESPACES_TAG_MATCH
        self._row_set_cls = ODSRowSet

    def make_tables(self):
        """
        Return the sheets in the workbook.

        A regex is used for this to avoid having to:

        1. load large the entire file into memory, or
        2. SAX parse the file more than once
        """
        namespace_tags = self._get_namespace_tags()
        sheets = [
            m.groups(0)[0] for m in self._table_matcher.finditer(self.content)
        ]
        return [
            self._row_set_cls(sheet, self.window, namespace_tags)
            for sheet in sheets
        ]

    def _get_namespace_tags(self):
        match = re.search(self._namespace_tag_matcher, self.content)
        assert match
        tag_open = match.groups()[0]
        tag_close = self._document_close_tag
        return tag_open, tag_close


class ODSRowSet(object):
    """ODS support for a single sheet in the ODS workbook. Unlike
    the CSV row set this is not a streaming operation."""

    def __init__(self, sheet, window=None, namespace_tags=None):
        self.sheet = sheet

        self.name = "Unknown"
        m = ODS_TABLE_NAME.match(self.sheet)
        if m:
            self.name = m.groups(0)[0]
            if not PY2 and isinstance(self.name, bytes):
                self.name = self.name.decode("utf-8")

        self.window = window or 1000

        # We must wrap the XML fragments in a valid header otherwise iterparse
        # will explode with certain (undefined) versions of libxml2. The
        # namespaces are in the ODS file, and change with the libreoffice
        # version saving it, so get them from the ODS file if possible. The
        # default namespaces are an option to preserve backwards compatibility
        # of ODSRowSet.
        if namespace_tags:
            self.namespace_tags = namespace_tags
        else:
            namespaces = DEFAULT_NAMESPACES

            ods_header = u"<wrapper {0}>".format(
                " ".join(
                    'xmlns:{0}="{1}"'.format(k, v)
                    for k, v in namespaces.iteritems()
                )
            ).encode("utf-8")
            ods_footer = u"</wrapper>".encode("utf-8")
            self.namespace_tags = (ods_header, ods_footer)

        self._row_matcher = ODS_ROW_MATCH

    def raw(self, sample=False):
        """ Iterate over all rows in this sheet. """
        rows = self._row_matcher.findall(self.sheet)

        for row in rows:
            row_data = []

            block = self.namespace_tags[0] + row + self.namespace_tags[1]
            partial = io.BytesIO(block)

            for action, element in etree.iterparse(partial, ("end",)):
                if element.tag != _tag(NS_OPENDOCUMENT_TABLE, TABLE_CELL):
                    continue

                cell = _read_cell(element)
                repeat = element.attrib.get(
                    _tag(NS_OPENDOCUMENT_TABLE, COLUMN_REPEAT)
                )

                if repeat:
                    number_of_repeat = int(repeat)
                    row_data += [cell] * number_of_repeat
                else:
                    row_data.append(cell)

            del partial
            yield row_data
        del rows


class FODSTableSet(ODSTableSet):
    """
    A wrapper around ODS files. Because they are zipped and the info we want
    is in the zipped file as content.xml we must ensure that we either have
    a seekable object (local file) or that we retrieve all of the content from
    the remote URL.
    """

    def __init__(self, fileobj, window=None, **kw):
        """Initialize the object.

        :param fileobj: may be a file path or a file-like object. Note the
        file-like object *must* be in binary mode and must be seekable (it will
        get passed to zipfile).

        As a specific tip: urllib2.urlopen returns a file-like object that is
        not in file-like mode while urllib.urlopen *does*!

        To get a seekable file you *cannot* use
        messytables.core.seekable_stream as it does not support the full seek
        functionality.
        """
        if hasattr(fileobj, "read"):
            self.content = fileobj.read()
        else:
            with open(fileobj, "rb") as f:
                self.content = f.read()

        self.window = window

        self._table_matcher = FODS_TABLE_MATCH
        self._document_close_tag = FODS_DOCUMENT_CLOSE_TAG
        self._namespace_tag_matcher = FODS_NAMESPACES_TAG_MATCH
        self._row_set_cls = FODSRowSet


class FODSRowSet(ODSRowSet):
    """ODS support for a single sheet in the ODS workbook. Unlike
    the CSV row set this is not a streaming operation."""

    def __init__(self, sheet, window=None, namespace_tags=None):
        super(FODSRowSet, self).__init__(sheet, window, namespace_tags)
        self._row_matcher = FODS_ROW_MATCH


def _read_cell(element):
    cell_type = element.attrib.get(_tag(NS_OPENDOCUMENT_OFFICE, VALUE_TYPE))
    value_token = VALUE_TOKEN.get(cell_type, "value")
    if cell_type == "string":
        cell = _read_text_cell(element)
    elif cell_type == "currency":
        value = element.attrib.get(_tag(NS_OPENDOCUMENT_OFFICE, value_token))
        currency = element.attrib.get(_tag(NS_OPENDOCUMENT_OFFICE, "currency"))
        cell = (value + " " + currency, "currency")
    elif cell_type is not None:
        value = element.attrib.get(_tag(NS_OPENDOCUMENT_OFFICE, value_token))
        cell = (value, cell_type)
    else:
        cell = ("", "string")
    return cell


def _read_text_cell(element):
    children = element.getchildren()
    text_content = []
    for child in children:
        text = "".join([x for x in child.itertext()])
        text_content.append(text)
    if len(text_content) > 0:
        cell_value = "\n".join(text_content)
    else:
        cell_value = ""
    return (cell_value, "string")


def _tag(namespace, tag):
    return "{%s}%s" % (namespace, tag)
