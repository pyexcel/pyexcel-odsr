#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os

import psutil
import pyexcel as pe
import pytest

from pyexcel_odsr import get_data

IN_TRAVIS = "TRAVIS" in os.environ


def test_bug_fix_for_issue_1():
    data = get_data(get_fixtures("repeated.ods"), library="pyexcel-odsr")
    assert data["Sheet1"] == [["repeated", "repeated", "repeated", "repeated"]]


def test_issue_14():
    # pyexcel issue 61
    test_file = "issue_61.ods"
    data = get_data(
        get_fixtures(test_file), skip_empty_rows=True, library="pyexcel-odsr"
    )
    assert data["S-LMC"] == [["aaa"], [0]]


def test_issue_1():
    test_file = "12_day_as_time.ods"
    data = get_data(
        get_fixtures(test_file), skip_empty_rows=True, library="pyexcel-odsr"
    )
    assert data["Sheet1"][0][0].days == 12


def test_issue_2():
    test_file = "multinode-in-a-p.ods"
    data = get_data(
        get_fixtures(test_file), skip_empty_rows=True, library="pyexcel-odsr"
    )
    assert data["product.template"][1][1] == "PRODUCT NAME PMP"


def test_issue_83_ods_file_handle():
    # this proves that odfpy
    # does not leave a file handle open at all
    proc = psutil.Process()
    test_file = get_fixtures("multinode-in-a-p.ods")
    open_files_l1 = proc.open_files()

    # start with a csv file
    data = pe.iget_array(file_name=test_file, library="pyexcel-odsr")
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
    pe.free_resources()
    open_files_l4 = proc.open_files()
    # this confirms that no more open file handle
    assert open_files_l1 == open_files_l4


def test_issue_23():
    if not IN_TRAVIS:
        pytest.skip()
    pe.get_book(
        url="https://github.com/pyexcel/pyexcel-ods/raw/master/tests/fixtures/white_space.ods",
        library="pyexcel-odsr",
    )
    # flake8: noqa


def get_fixtures(filename):
    return os.path.join("tests", "fixtures", filename)
