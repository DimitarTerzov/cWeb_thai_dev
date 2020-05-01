# -*- coding: utf-8 -*-
from __future__ import print_function

from utils import temporary_file
from command_11.validator_11 import command11


CONTENT = [
    u'<!DOCTYPE Trans SYSTEM "trans-14.dtd">\n',                                  # 0
    u'<Section type="report" startTime="0" endTime="3215.909">\n',   # 1
    u'Säger jag [noise] #eh invandrare så uppstår det invandrare.De fanns innan jag sa det.\n',    # 2
    u'The ,#uh heat uh the heat up there here.\n',                                                                            # 3
    u'And this was a nice overall win Shane, a lot of people picking Baylor to win this game.\n',     # 4
    u'And this was a nice overall win Shane,a lot of people picking Baylor to win this game.\n',      # 5
    u'And this was a nice overall win Shane , a lot of people picking Baylor to win this game.\n',    # 6
    u"So, it's not gonna be just a one-man show.\n",     # 7
    u"So, it's not gonna be just a one - man show.\n",   # 8
    u"So, it's not gonna be just a one -man show.\n",    # 9
    u"So, it's not gonna be just a one- man show.\n",    # 10
    u"All right, Shane.  Well, let's kick it over.\n",          # 11
]
EXCLUDE = [
    0, 1, 4, 7, 8, 10
]
CATCH = [
    2, 3, 5, 6, 9, 11
]


def test_command_11(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command11(file_)

    for key in sorted(found.keys()):
        print(key, found[key])

    for row in EXCLUDE:
        assert row not in found

    for row in CATCH:
        assert row in found

    #assert 0
