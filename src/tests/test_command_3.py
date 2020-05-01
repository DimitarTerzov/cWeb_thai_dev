# -*- coding: utf-8 -*-
from __future__ import print_function

from command_3.validator_3 import command3
from utils import temporary_file


CONTENT = [
    u'ทางไปรษณีย์เป็นต้น [overlap] [overlap]\n',                     # 0
    u'อีกทั้งพลังงานภาคการผลิตต่าง [overlap] ๆ [overlap]\n',    # 1
    u'[music]\n',                                                                  # 2
    u'We have the order up here [lipsmack] and we believe\n',                 # 3
    u'#uh [cough] sorry, school counselor candidate too [cough]\n',         # 4
    u'#uh [cough] sorry, school counselor candidate too [coughy]\n',       # 5
    u'[sta] Velkommen til [sta] Troldespejlet Podcast nummer tolv,\n',      # 6
    u'[sta] [stay] Velkommen til Troldespejlet Podcast nummer tolv,\n',    # 7
    u'[breath]Et ega sul ju seal [breath] Otepää majal ma ei tea, kui tugev katus on.\n',    # 8
    u'[breath] Et ega sul ju seal[breath] Otepää majal ma ei tea, kui tugev katus on.\n',    # 9
    u'[breath] Et ega sul ju seal[breath]Otepää majal ma ei tea, kui tugev katus on.\n',    # 10
]
EXCLUDES = [1, 2, 3, 4, 6]
CATCHES = [0, 5, 7, 8, 9, 10]


def test_command_3(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command3(file_)

    for key in sorted(found.keys()):
        print(key, found[key])

    for item in EXCLUDES:
        assert item not in found

    for item in CATCHES:
        assert item in found

    #assert 0
