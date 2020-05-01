# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from utils import temporary_file
from command_13.validator_13 import command13


CONTENT = [
    u'<Turn startTime="0" endTime="1.351">\n',                         # 1
    u'<Sync time="0"/>\n',                                             # 2
    u'[music]\n',                                                      # 3
    u'</Turn>\n',                                                      # 4
    u'<Turn speaker="spk2" startTime="1.351" endTime="10.959">\n',     # 5
    u'<Sync time="1.351"/>\n',                                         # 6
    u'&lt;lang:Foreign&gt; (()) &lt;/lang:Foreign&gt;\n',              # 7
    u'<Sync time="5.854"/>\n',                                         # 8
    u'[music]\n',                                                      # 9
    u'</Turn>\n',                                                      # 10
    u'<Turn startTime="10.959" endTime="55.643" speaker="spk2">\n',    # 11
    u'<Sync time="10.959"/>\n'                                                       # 12
    u"Welcome to Insight, I'm Philippa Tolley. This week, the Pacific.\n",           # 13
    u'<Sync time="22.275"/>\n',                                                      # 14
    u'Its Prime Minister has been vocal on the world stage, trying to\n',            # 15
    u'<Sync time="32.566"/>\n',                                                      # 16
    u'But despite that gloomy outlook, the low line group of atolls and\n',          # 17
    u'<Sync time="41.26"/>\n',                                                       # 18
    u'Tuvalu has big plans for its future and its leaders that urging.\n',           # 19
    u'<Sync time="49.963"/>\n',                                                      # 20
    u'[music]\n',                                                                    # 21
    u'<Sync time="51.747"/>\n',                                                      # 22
    u'[noise]\n',                                                                    # 23
    u'</Turn>\n',                                                                    # 24
    u'<Turn speaker = " spk4 " startTime="55.643" endTime="112.245">\n',             # 25
    u'<Sync time="55.643"/>\n',                                                      # 26
    u"I bounce on the Funafuti lagoon. It seems a world away from Fulafani.\n",      # 27
    u'<Sync time="67.998"/>\n',                                                      # 28
    u"Behind me, I can just see a narrow strip of land peeping above the water.\n",  # 29
    u'<Sync time="78.971"/>\n',                                                      # 30
    u'[noise]\n',                                                           # 31
    u'<Sync time="81.713"/> \n',                                            # 32
    u'<Sync time="91.488"/>\n',                                             # 33
    u'\n',                                                                 # 34
    u'<Sync time="101.239"/>\n',                                            # 35
    u'</Turn>\n',                                                           # 36
    u'<Turn startTime="114.68" endTime="135.900">\n',                       # 37
    u'<Sync time="114.68"/>\n',                                             # 38
    u'</Turn>\n',                                                           # 39
    u'<Turn speaker="spk4" startTime="138.482" endTime="152.316">\n',       # 40
    u'<Sync time="138.482"/>\n',                                            # 41
    u'\n',                                                                 # 42
    u'</Turn>\n',                                                           # 43
    u'<Turn speaker="spk5" startTime="152.316" endTime="156.423">\n',       # 44
    u'<Sync time="152.316"/>\n',                                            # 45
    u'&lt;lang:Foreign&gt; (()) &lt;/lang:Foreign&gt;\n',                   # 46
    u'</Turn>\n',                                                           # 47
    u'<Turn speaker="spk5" startTime="160.404" endTime="161.589">\n',       # 48
    u'<Sync time="160.404"/>\n',                                            # 49
    u'&lt;lang:Foreign&gt; (()) &lt;/lang:Foreign&gt;\n',                   # 50
    u'</Turn>\n',                                                           # 51
    u'<Turn speaker="spk4" startTime="197.187" endTime="210.034">\n',       # 52
    u'<Sync time="197.187"/>\n',                                            # 53
    u"Mr. ((Lucia)) has to go further out into the lagoon to get fish.\n",  # 54
    u'<Sync time="208.49"/>\n',                                             # 55
    u'</Turn>\n',                                                           # 56
    u'<Turn startTime="210.034" endTime="211.351">\n',                      # 57
    u'<Sync time="210.034"/>\n',                                            # 58
    u'\n',                                                                 # 59
    u'</Turn>\n',                                                           # 60
    u'<Turn speaker="spk64" startTime="3391.391" endTime="3391.334">\n',    # 61
    u'<Sync time="3391.391"/>\n',                                           # 62
    u'김아영씨 저희가 심폐소생 해드렸습니다.\n',                               # 63
    u'</Turn>\n',                                                           # 64
    u'<Turn speaker="spk4" startTime="197.187" endTime="210.034">\n',       # 65
    u'<Sync time="196.187"/>\n',                                            # 66
    u"Mr. ((Lucia)) has to go further out into the lagoon to get fish.\n",  # 67
    u'</Turn>\n',                                                           # 68
    u'<Turn speaker="spk5" startTime =" 197.187 " endTime= " 210.034 ">\n', # 69
    u'<Sync time=" 196.187"/>\n',                                           # 70
    u"Mr. ((Lucia)) has to go further out into the lagoon to get fish.\n",  # 71
    u'<Sync time= "197.187"/>\n',                                           # 72
    u"Mr. ((Lucia)) has to go further out into the lagoon to get fish.\n",  # 73
    u'<Sync time ="197.187"/>\n',                                           # 74
    u"Mr. ((Lucia)) has to go further out into the lagoon to get fish.\n",  # 75
    u'</Turn>\n',                                                           # 76
    u'<Turn speaker ="spk6" startTime=" 197.187" endTime="210.034 ">\n',    # 77
    u'<Sync time="197.187"/>\n',                                            # 78
    u"Mr. ((Lucia)) has to go further out into the lagoon to get fish.\n",  # 79
    u'<Sync time="197.187 "/>\n',                                           # 80
    u"Mr. ((Lucia)) has to go further out into the lagoon to get fish.\n",  # 81
    u'</Turn>    \n',                                                       # 82
    u'<Turn startTime="454.698" endTime="460.184">\n',                      # 83
    u'<Sync time=" 454.698"/>\n',                                           # 84
    u'[no-speech]\n',                                                       # 85
    u'<Sync time="459.292"/>\n',    # 86
    u'\n',                                            # 87
    u'Oh, man. One of our greatest white allies and one of the [laugh]\n',    # 88
    u'<Sync time="460.100"/>\n',    # 89
    u'Oh, man. One of our greatest white allies and one of the [laugh]\n',    # 90
    u'\n',                                                                                      # 91
    u'<Sync time="460.424"/>\n',                                            # 92
    u'[no-speech]\n',                                                       # 93
    u'<Sync time="462.832"/>\n',                                            # 94
    u'Sync Ike Rann ja tema uus album &lt;lang:English&gt; Synchronize &lt;/lang:English&gt; Me kuulame\n',  # 95
    u'</Turn>\n',                                                           # 96
]

EXCLUDE_ROWS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 34, 36, 39,
                42, 43, 44, 45, 46, 47, 49, 50, 51, 53, 54, 56, 57, 59, 60, 62,
                63, 64, 67, 68, 71, 72, 73, 75, 76, 78, 79, 81, 82, 84, 85, 86, 87,
                88, 89, 90, 91, 93, 95, 96]


def test_command_13(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command13(file_)

    for key in sorted(found.keys()):
        print(key, found[key])

    for row in EXCLUDE_ROWS:
        assert row not in found

    assert "Sequential turns by the same speaker" in found[11]
    assert "Empty segments are not allowed" in found[32]
    assert "Empty segments are not allowed" in found[33]
    assert "Empty segments are not allowed" in found[35]
    assert "Turn out of sync" in found[37]
    assert "Empty segments are not allowed" in found[38]
    assert "Turn out of sync" in found[40]
    assert "Empty segments are not allowed" in found[41]
    assert "Sequential turns by the same speaker" in found[48]
    assert "Turn out of sync" in found[52]
    assert "Empty segments are not allowed" in found[55]
    assert "Empty segments are not allowed" in found[58]
    assert "Turn out of sync" in found[61]
    assert "Turn out of sync" in found[65]
    assert "Segment out of sync" in found[66]
    assert "Turn out of sync" in found[69]
    assert "Segment out of sync" in found[70]
    assert "Segment out of sync" in found[74]
    assert "Turn out of sync" in found[77]
    assert "Segment out of sync" in found[80]
    assert "Turn out of sync" in found[83]
    assert "Segment out of sync" in found[92]
    assert "Segment out of sync" in found[94]

    #assert 0
