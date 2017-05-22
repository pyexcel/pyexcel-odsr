"""
    pyexcel_odsr
    ~~~~~~~~~~~~~~~~~~~
    The lower level ods file format handler using messytables
    :copyright: (c) 2015-2017 by Onni Software Ltd & its contributors
    :license: New BSD License
"""
# flake8: noqa
# this line has to be place above all else
# because of dynamic import
from pyexcel_io.plugins import IOPluginInfoChain
from pyexcel_io.io import get_data as read_data, isstream, store_data as write_data

__FILE_TYPE__ = 'ods'
IOPluginInfoChain(__name__).add_a_reader(
    relative_plugin_class_path='odsr.ODSBook',
    file_types=[__FILE_TYPE__],
    stream_type='binary'
)


from pyexcel_io.io import get_data as read_data, isstream


def get_data(afile, file_type=None, **keywords):
    """standalone module function for reading module supported file type"""
    if isstream(afile) and file_type is None:
        file_type = __FILE_TYPE__
    return read_data(afile, file_type=file_type, **keywords)
