# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from utils import temporary_file
from command_7.validator_7 import command7


CONTENT = [
    u'<Speaker id="spk75" name="speaker#56" check="no" type="female" dialect="native" accent="" scope="local"/>\n', # 1
    u'<Speaker id="spk76" name="speaker#57" check="no" type="female" dialect="native" accent="" scope="local"/>\n', # 2
    u'<Section type="report" startTime="0" endTime="2631.216">\n' # 3
    u'คิดว่า #อ่า ไปที่เดียวได้สองเจ้าเลย\n', # 4
    u'#เอ่อ มีครับ คือบทเรียนที่หนักที่สุดของเขาเกิดขึ้นเมื่อ\n', # 5
    u'ใช่ ใช่ ใช่ อยู่ใน #อือ ค่อนข้างจะเป็นส่วนกลางของกรุงปักกิ่งในปัจจุบันแล้วค่ะ\n', # 6
    u'#อืม ชนเผ่าชาวปศุสัตว์หรือว่าชนเผ่าส่วนน้อยหลายๆชนเผ่าด้วย\n', # 7
    u'#อือ ตามความเข้าใจของตันตันนะคะไม่ค่อยมีบรรยากาศแบบสงบของ\n', # 8
    u'ตามความเข้า #ใจ ของตันตันนะคะ\n', # 9 no
    u'ใช่ค่ะ่ยงแล้วเพราะว่าขึ้นชื่ออยู่แล้วแล้วก็ #อือ ตามความเข้าใจของตันตันนะคะ\n', #10
    u'งนะคะก็เลยได้รวบรวมผู้เชี่ยวชาญแล้วก็ #อ่า ผู้แทนของชาวบ้าน\n', # 11
    u'งนะคะก็เลยได้รวบรวมผู้เชี่ยวชาญแ  #นข องชาวบ้าน\n', # 12 no
    u'ซึ่งตอนนี้นะคะที่นี่ก็ยังมีสถานที่แนะนำ #เอ่อ วัฒนธรรมและ\n', # 13
    u'</Section>'                                # 14
]

EXCLUDE = [
  1, 2, 3, 4, 5, 6,
  7, 8, 10, 11, 13, 14
]
CATCH = [9, 12]


def test_command_7(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command7(file_)

    keys = sorted(found.keys())
    for key in keys:
        print(key, found[key])

    for key in EXCLUDE:
        assert key not in found

    for key in CATCH:
        assert key in found

    #assert 0
