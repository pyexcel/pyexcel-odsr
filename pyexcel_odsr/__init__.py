"""
    pyexcel_odsr
    ~~~~~~~~~~~~~~~~~~~
    The lower level ods file format handler using messytables
    :copyright: (c) 2015-2017 by Onni Software Ltd & its contributors
    :license: New BSD License
"""
from pyexcel_io.plugins import IOPluginInfoChain
from pyexcel_io.io import get_data as read_data, isstream
from pyexcel_odsr._version import __version__, __author__  # flake8: noqa

__FILE_TYPE__ = 'ods'
__FILE_TYPE_FODS__ = 'fods'

IOPluginInfoChain(__name__).add_a_reader(
    relative_plugin_class_path='odsr.ODSBook',
    file_types=[__FILE_TYPE__],
    stream_type='binary'
).add_a_reader(
    relative_plugin_class_path='odsr.FODSBook',
    file_types=[__FILE_TYPE_FODS__],
    stream_type='binary'
)


def get_data(afile, file_type=None, **keywords):
    """standalone module function for reading module supported file type"""
    if isstream(afile) and file_type is None:
        file_type = __FILE_TYPE__
    return read_data(afile, file_type=file_type, **keywords)
