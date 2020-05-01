# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from command_15.validator_15 import command15
from utils import temporary_file


CONTENT =[
    u"Č~word\n",      # 0
    u"word ~ word\n",    # 1
    u"Č~~ word\n",    # 2
    u"word~ word\n",     # 3
    u"hello world~word\n",      # 4
    u"word ~word\n",            # 5
    u" ~word\n",                # 6
    u"hello word~ word\n",      # 7
    u"hello word~ .\n",         # 8
    u"hello world~.\n",         # 9
    u"hello hello~, Where\n",   # 10
    u" ~ word\n",               # 11
    u"word ~ \n",               # 12
    u"hello ~~.\n",             # 13
    u"~~hi\n",                  # 14
    u"where ~Tilde milde\n",              # 15
    u"So,~ not allowed\n",                  # 16
    u"also .~ not allowed\n",               # 17
    u"this ,~. too not allowed\n",         # 18
    u"filler #uh~ tilde not allowed\n"   # 19
    u"filler #uhaa~. dot\n"                   # 20
    u"filler #uha~a bla\n"                     # 21
    u"[noise]~. ala bala\n"                    # 22
    u"ala ~. bala\n",                              # 23
    u",~. bala\n",                                   # 24
    u"~. alabala\n",                               # 25
    u"~ Čhalai babuli\n",                       # 26
    u'of &lt;initial&gt; U &lt;/initial&gt;~ people\n'    # 27
]


def test_command15(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command15(file_)

    keys = sorted(found.keys())
    for key in keys:
        print(key, found[key])

    assert "Č~word" in found[0]
    assert "word ~ word" in found[1]
    assert "Č~~ word" in found[2]
    assert "world~word" in found[4]
    assert not 9 in found
    assert not 10 in found
    assert " ~ word" in found[11]
    assert "word ~ " in found[12]
    assert "hello ~~" in found[13]
    assert "~~hi" in found[14]
    assert not 15 in found
    assert "So,~" in found[16]
    assert ".~" in found[17]
    assert ",~." in found[18]
    assert "#uh~" in found[19]
    assert "#uhaa~" in found[20]
    assert "#uha~" in found[21]
    assert "[noise]~." in found[22]
    assert "~." in found[23]
    assert ",~." in found[24]
    assert "~." in found[25]
    assert "~ " in found[26]
    assert 27 not in found
    assert len(found) == 19

    #assert 0
