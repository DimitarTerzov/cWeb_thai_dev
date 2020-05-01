# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from utils import temporary_file
from command_22.validator_22 import command22


CONTENT = [
    u'<Speakers>\n',
    u'<Speaker id="spk1" name="Paul Donato" check="no" type="male" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk2" name="Henry Milorin" check="no" type="male" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk3" name="Mike Ruggiero" check="no" type="female" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk4" name="multiple" check="no" type="unknown" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk5" name="Mike Ruggiero" check="no" type="male" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk6" name="Jenny Graham" check="no" type="female" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk7" name="Melanie McLaughlin" check="no" type="female" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk8" name="Robert Skerry Jr" check="no" type="male" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk9" name="Mea Quinn Mustone" check="no" type="female" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk10" name="Cheryl Rodriguez" check="no" type="female" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk11" name="John Intoppa" check="no" type="male" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk12" name="Kathleen Kreatz"\n',
    u'check="no" type="female" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk13" name="Paulette Van der Kloot" check="no" type="female" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk14" name="Paul Ruseau" check="no" type="male" dialect="native" accent="" scope="global"/>\n',
    u'</Speakers>\n',
    u'<Episode>\n',
    u'<Section type="report" startTime="0" endTime="3489.288">\n',
    u'<Speaker id="spk1" name="Paul Donato" check="no" type="male" dialect="native" accent="" scope="global"/>\n',
    u'<Speaker id="spk2" name="Henry Milorin" check="no" type="male" dialect="native" accent="" scope="global"/>'
]


def test_command_22(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command22(file_)

    for key in sorted(found.keys()):
        print(key, found[key])

    #assert 0
