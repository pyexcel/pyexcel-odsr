#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import psutil
import pyexcel as pe
from pyexcel_odsr import get_data
from nose.tools import raises, eq_


def test_bug_fix_for_issue_1():
    data = get_data(get_fixtures("repeated.ods"),
                    library='pyexcel-odsr')
    eq_(data["Sheet1"], [['repeated', 'repeated', 'repeated', 'repeated']])


def test_date_util_parse():
    from pyexcel_odsr.converter import date_value
    value = "2015-08-17T19:20:00"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:00"
    value = "2015-08-17"
    d = date_value(value)
    assert d.strftime("%Y-%m-%d") == "2015-08-17"
    value = "2015-08-17T19:20:59.999999"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:59"
    value = "2015-08-17T19:20:59.99999"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:59"
    value = "2015-08-17T19:20:59.999999999999999"
    d = date_value(value)
    assert d.strftime("%Y-%m-%dT%H:%M:%S") == "2015-08-17T19:20:59"


@raises(Exception)
def test_invalid_date():
    from pyexcel_odsr.converter import date_value
    value = "2015-08-"
    date_value(value)


@raises(Exception)
def test_fake_date_time_10():
    from pyexcel_odsr.converter import date_value
    date_value("1234567890")


@raises(Exception)
def test_fake_date_time_19():
    from pyexcel_odsr.converter import date_value
    date_value("1234567890123456789")


@raises(Exception)
def test_fake_date_time_20():
    from pyexcel_odsr.converter import date_value
    date_value("12345678901234567890")


def test_issue_14():
    # pyexcel issue 61
    test_file = "issue_61.ods"
    data = get_data(get_fixtures(test_file),
                    skip_empty_rows=True, library='pyexcel-odsr')
    eq_(data['S-LMC'], [[u'aaa'], [0]])


def test_issue_1():
    test_file = "12_day_as_time.ods"
    data = get_data(get_fixtures(test_file),
                    skip_empty_rows=True, library='pyexcel-odsr')
    eq_(data['Sheet1'][0][0].days, 12)


def test_issue_1_error():
    from pyexcel_odsr.converter import time_value
    result = time_value('PT1111')
    eq_(result, None)


def test_issue_2():
    test_file = "multinode-in-a-p.ods"
    data = get_data(get_fixtures(test_file),
                    skip_empty_rows=True, library='pyexcel-odsr')
    eq_(data['product.template'][1][1], 'PRODUCT NAME PMP')


def test_issue_83_ods_file_handle():
    # this proves that odfpy
    # does not leave a file handle open at all
    proc = psutil.Process()
    test_file = get_fixtures("multinode-in-a-p.ods")
    open_files_l1 = proc.open_files()

    # start with a csv file
    data = pe.iget_array(file_name=test_file, library='pyexcel-odsr')
    open_files_l2 = proc.open_files()
    delta = len(open_files_l2) - len(open_files_l1)
    # cannot catch open file handle
    assert delta == 0

    # now the file handle get opened when we run through
    # the generator
    list(data)
    open_files_l3 = proc.open_files()
    delta = len(open_files_l3) - len(open_files_l1)
    # cannot catch open file handle
    assert delta == 0

    # free the fish
    pe.free_resource()
    open_files_l4 = proc.open_files()
    # this confirms that no more open file handle
    eq_(open_files_l1, open_files_l4)


def get_fixtures(filename):
    return os.path.join("tests", "fixtures", filename)
