# -*- coding: utf-8 -*-
from __future__ import print_function

from utils import temporary_file
from command_25.validator_25 import command25


CONTENT = [
    u'<Turn startTime="0" endTime ="14.781" speaker="spk1">\n',    # 1
    u'<Syncs time="0"/>\n',                                         # 2
    u'[overlap]\n'                                                 # 3
    u'</Turn>\n',                                                  # 4
    u'<Turn speaker="spk2" startTime="14.781" endTime=" 21.081">\n',  # 5
    u'<Sync time=" 15.781"/>\n',                                      # 6
    u'[noise] [music] 물러나시오! 임금님 행차하신다.\n',                # 7
    u'</Turn>\n',                                                     # 8
    u'<Turn speaker="spk3" startTime="21.081 " endTime="32.282">\n',  # 9
    u'<Sync time= "28.081"/>\n',                                      # 10
    u'[laugh] [applause] 보이느냐? 나의 이 멋진 옷이! [laugh]\n',       # 11
    u'</Turn>\n',                                                     # 12
    u'<Turn speaker="spk4" startTime="32.282" endTime="39.087 ">\n',  # 13
    u'<Sync time=" 32.282"/>\n',                                      # 14
    u'오, 그렇다면 나는 랜덤 캐릭터. [noise]\n',                        # 15
    u'</Turn>\n',                                                     # 16
    u'<Turn speaker="spk5 " startTime="39.087" endTime="43.950">\n',  # 17
    u'<Sync time="39.087 "/>\n',                                      # 18
    u'아, 이 아저씨가 여기서 또 옷 벗고 있네? 따라와요.\n',              # 19
    u'</Turn>\n',                                                     # 20
    u'<Turn speaker=" spk1" startTime="43.950" endTime="58.756">\n',  # 21
    u'<Sync time= "43.950"/>\n',                                      # 22
    u'[overlap]\n',                                                   # 23
    u'</Turn>\n',                                                     # 24
    u'<Turn speaker= "spk6" startTime="58.756" endTime="68.486">\n',  # 25
    u'<Sync time ="58.756"/>\n',                                              # 26
    u'[music] 아하. [noise] 어, 우와. 내 머리는 길지만 니 수명을 짧을 거야.\n',  # 27
    u'</Turn>\n',                                                             # 28
    u'<Turn speaker="spk2" startTime="956.003" endTime="957.894">\n',         # 29
    u'<Sync time="59.003"/>\n',                                               # 30
    u'Thank you candidate Graham. [overlap] Thanks.\n',                       # 31
    u'</Turn>\n',                                                             # 32
    u'<Turn speaker ="spk4" startTime="68.486" endTime="73.614">\n',          # 33
    u'<Sync tme="68.486"/>\n',                                                # 34
    u'[laugh] 그래. 그럼 나는 영화 어 아저씨의 멋있는 원빈! [noise]\n',          # 35
    u'</Turn>\n',                                                             # 36
    u'<Turn startTime ="3170.236" endTime="3171.857">\n',                     # 37
    u'<Sync time="3170.236"/>\n',                                             # 38
    u'[noise] &lt;lang:Foreign&gt;ČSSDspacing 5ČSSD &lt;/lang:Foreign&gt;\n', # 39
    u'</Turn>\n',                                                             # 40
    u'<Turn startTime= "3170.236" endTime="3171.857">\n',                     # 41
    u'<Turn startTime=" 3170.236" endTime="3171.857">\n',                     # 42
    u'<Turn startTime="3170.236 " endTime="3171.857">\n',                     # 43
    u'<Turn startTime ="3170.236" endTime="3171.857">\n',                     # 44
    u'<Turn startTime="3170.236" endTime= "3171.857">\n',                     # 45
    u'<Turn startTime="3170.236" endTime="3171.857" speaker="spk2 ">\n',      # 46
    u'<Turn startTime="3170.236" endime="3171.857" speaker="spk2">\n',        # 47
    u'<Turn speaker="spk2" starterTime="3170.236" endTime="3171.857">\n',     # 48
    u'<Turn speakers="spk2" startTime="3170.236" endTime="3171.857">\n',      # 49
    u'<Turns speaker="spk2" startTime="3170.236" endTime="3171.857">\n',      # 50
    u'<Turn startTime="3170.236" endTime="3171.857" speaker="spker2">\n',     # 51
    u'<Speaker id="spk1" name="Paul Donato" check="no" type="male" dialect="native" accent="" scope="global"/>\n',   # 52
    u'<Speaker id="spk2" name="Henry Milorin" check="no" type="male" dialect="native" accent="" scope="global"/>\n', # 53
    u'<Speaker id="spk12" name="Kathleen Kreatz" \n',                                                                # 54
    u'check="no" type="female" dialect="native" accent="" scope="global"/>\n',                                       # 55
    u'<Speaker id="spk3" name="Mike Ruggiero" check="no" type="female" dialect="native" accent="" scope="global"/>\n'# 56

    u'<Turn speaker="spk2" startTime="3170.236" endTime="3171.857">\n',    # 57
    u'<Sync time="58.756"/>\n',                                 # 58
    u'\n',                                                                        # 59
    u'[music] 아하. [noise] 어, 우와. 수명을 짧을 거야.\n',    # 60
    u'</Turn>\n',                                                           # 61
    u'<Turn speaker="spk2" startTime="3170.236" endTime="3171.857">\n',    # 62
    u'<Sync time="58.756"/>\n',                                 # 63
    u'[music] 아하. [noise] 어, 우와.\n',                             # 64
    u'\n',                                                                         # 65
    u'<Sync time="58.756"/>\n',                                  # 66
    u'[music] 아하. [noise] 어, 우와.\n',                             # 67
    u'<Sync time="0"/>\n',                                           # 68
    u'\n',                                                                         # 69
    u'<Sync time="0"/>\n',                                           # 70
    u'\n',                                                                         # 71
    u'</Turn>\n'                                                             # 72
]


def test_command25(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command25(file_)

    for key in sorted(found.keys()):
        print(key, found[key])

    assert "Unexpected white space in Turn tag" in found[1]
    assert 'Tag syntax error' in found[2]
    assert not 3 in found
    assert not 4 in found
    assert "Unexpected white space in Turn tag" in found[5]
    assert "Unexpected white space in Sync tag" in found[6]
    assert not 7 in found
    assert not 8 in found
    assert "Unexpected white space in Turn tag" in found[9]
    assert "Unexpected white space in Sync tag" in found[10]
    assert not 11 in found
    assert not 12 in found
    assert "Unexpected white space in Turn tag" in found[13]
    assert "Unexpected white space in Sync tag" in found[14]
    assert not 15 in found
    assert not 16 in found
    assert "Unexpected white space in Turn tag" in found[17]
    assert "Unexpected white space in Sync tag" in found[18]
    assert not 19 in found
    assert not 20 in found
    assert "Unexpected white space in Turn tag" in found[21]
    assert "Unexpected white space in Sync tag" in found[22]
    assert not 23 in found
    assert not 24 in found
    assert "Unexpected white space in Turn tag" in found[25]
    assert "Unexpected white space in Sync tag" in found[26]
    assert not 27 in found
    assert not 28 in found
    assert not 29 in found
    assert not 30 in found
    assert not 31 in found
    assert not 32 in found
    assert "Unexpected white space in Turn tag" in found[33]
    assert "Tag syntax error" in found[34]
    assert not 35 in found
    assert not 36 in found
    assert "Unexpected white space in Turn tag" in found[37]
    assert 38 not in found
    assert not 39 in found
    assert not 40 in found
    assert "Unexpected white space in Turn tag" in found[41]
    assert "Unexpected white space in Turn tag" in found[42]
    assert "Unexpected white space in Turn tag" in found[43]
    assert "Unexpected white space in Turn tag" in found[44]
    assert "Unexpected white space in Turn tag" in found[45]
    assert "Unexpected white space in Turn tag" in found[46]
    assert "Tag syntax error" in found[47]
    assert "Tag syntax error" in found[48]
    #assert 49 in found
    assert "Tag syntax error" in found[50]
    #assert 51 in found
    assert 52 not in found
    assert 53 not in found
    assert "Tag syntax error" in found[54]
    assert 55 not in found
    assert 56 not in found
    assert "Empty row in Sync tag" in found[59]
    assert "Empty row in Sync tag" in found[65]
    assert 57 not in found
    assert 58 not in found
    assert 60 not in found
    assert 61 not in found
    assert 62 not in found
    assert 63 not in found
    assert 64 not in found
    assert 66 not in found
    assert 67 not in found
    assert 68 not in found
    assert 69 not in found
    assert 70 not in found
    assert 71 not in found
    assert 72 not in found

    #assert 0
