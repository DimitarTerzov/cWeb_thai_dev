# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from utils import temporary_file
from command_14.command_14 import command14


CONTENT = [
    u'<Section type="report" startTime="0" endTime="178.793">\n'    # 0
    u'<Turn startTime="0" endTime="135.900">\n',                        # 1
    u'<Sync time="0"/>\n',                                                                # 2
    u'</Turn>\n',                                                                                          # 3
    u'<Turn speaker="spk5" startTime="135.900" endTime="138.482">\n', # 4
    u'<Sync time="14.900"/>\n',                                                               # 5
    u'&lt;lang:Foreign&gt;incorrect (()) &lt;/lang:Foreign&gt;\n'                  # 6
    u'</Turn>\n',                                                                                              # 7
    u'<Turn startTime="138.482" endTime="152.316">\n',                       # 8
    u'<Sync time="138.482"/>\n',                                                               # 9
    u'</Turn>\n'                                                                                            # 10
    u'<Turn speaker="spk5" startTime="152.316" endTime="178.793">\n', # 11
    u'<Sync time="152.316"/>\n',                                                                    # 12
    u'word&lt;lang:Foreign&gt; (()) before&lt;/lang:Foreign&gt;\n',                   # 13
    u'</Turn>\n',                                                                                               # 14
    u'</Section>\n'                                                                                            # 15
]
EXCLUDE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 14, 15]
CATCH = [9, 12]

def test_command_14(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command14(file_)

    for key in sorted(found.keys()):
        print(key, found[key])

    for row in EXCLUDE:
        assert row not in found

    for row in CATCH:
        assert row in found

    #assert 0
