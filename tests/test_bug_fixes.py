#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
from pyexcel_odsr import get_data
from nose.tools import raises, eq_


def test_bug_fix_for_issue_1():
    data = get_data(os.path.join("tests", "fixtures", "repeated.ods"),
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
    data = get_data(os.path.join("tests", "fixtures", test_file),
                    skip_empty_rows=True, library='pyexcel-odsr')
    eq_(data['S-LMC'], [[u'aaa'], [0]])


def test_issue_1():
    test_file = "12_day_as_time.ods"
    data = get_data(os.path.join("tests", "fixtures", test_file),
                    skip_empty_rows=True, library='pyexcel-odsr')
    eq_(data['Sheet1'][0][0].days, 12)


def test_issue_1_error():
    from pyexcel_odsr.converter import time_value
    result = time_value('PT1111')
    eq_(result, None)


def test_issue_19():
    test_file = "pyexcel_81_ods_19.ods"
    data = get_data(os.path.join("tests", "fixtures", test_file),
                    skip_empty_rows=True, library='pyexcel-odsr')
    eq_(data['product.template'][1][1], 'PRODUCT NAME PMP')
