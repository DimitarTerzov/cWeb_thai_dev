# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from utils import temporary_file
from command_14.command_14 import command14


CONTENT = [
    u'<Sync time= "0"/>\n',         # 1
    u'<Sync time=" 81.713"/>\n',    # 2
    u'<Sync time="91.488 "/>\n',    # 3
    u'<Sync time ="107.239"/>\n',   # 4
    u'<Sync time="114.68"/>\n',    # 5
    u'<Sync time="135.900" />'      # 6
]


def test_command_14(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command14(file_)

    for key in sorted(found.keys()):
        print(key, found[key])

    assert 1 not in found
    assert 2 in found
    assert 3 not in found
    assert 4 in found
    assert 5 not in found
    assert 6 in found

    #assert 0
