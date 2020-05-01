# -*- coding: utf-8 -*-
from __future__ import print_function

from command_17.validator_17 import command17
from tests.utils import temporary_file


CONTENT = [
    u'<Turn speaker="spk1" startTime="5.151" endTime="21.878">\n',    # 1
    u'<Sync time="5.151"/>\n',                                                                     # 2
    u'В емисията ще видите.\n',                                                                   # 3
    u'<Sync time="6.434"/>\n',                                                                    # 4
    u'Обсъждат менюто в училищните столове в Бургас.\n',                     # 5
    u'</Turn>\n',                                                                                             # 6
    u'<Turn startTime="21.878" endTime="24.816">\n',                              # 7
    u'<Sync time="21.878"/>\n',                                                                    # 8
    u'[music]\n',                                                                                               # 9
    u'</Turn>\n',                                                                                             # 10
    u'<Turn speaker="spk1" startTime="24.816" endTime="35.97">\n',      # 11
    u'<Sync time="24.816"/>\n',                                                                    # 12
    u'Поредно нападение над спешен екип в ромска махала.\n',              # 13
    u'<Sync time="29.434"/>\n',                                                                     # 14
    u'Обсъждат менюто в училищните столове в Б    ургас.\n',                  # 15
    u'<Sync time="31.434"/>\n',                                                                     # 16
    u'Обсъждат менюто в училищните столове в Б    ургас.\n',                  # 17
    u'</Turn>\n',                                                                                              # 18
]
EXCLUDE = [
    1, 3, 4, 5, 6, 7, 9, 10, 11,
    12, 13, 15, 16, 17, 18
]
CATCH = [2, 8, 14]


def test_command_17(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command17(file_)

    for key in sorted(found.keys()):
        print(key, found[key])

    for row in EXCLUDE:
        assert row not in found

    for row in CATCH:
        assert row in found

    #assert 0
