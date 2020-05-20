# -*- coding: utf-8 -*-
from __future__ import print_function

from utils import temporary_file
from command_26.validator_26 import command26


CONTENT = [
    u'<Section type="report" startTime="0" endTime="600.000">\n',
    u'<Turn startTime="0" endTime="34.375" speaker="spk1">\n',
    u'<Sync time="0"/>\n',
    u'Hii ni dira ya dunia kutoka. idhaa ya. Kiswahili ya \
&lt;initial&gt; BBC &lt;/initial&gt;. Tuliyo nayo usiku huu. \n',
    u'<Sync time="8.504"/>\n',
    u'Hukumu ya kifo kwa. wanaume. wanne waliopatwa na hatia ya \
kumbaka na kisha kumwua. mwanamke huko India. \n',
    u'<Sync time="16.719"/>\n',
    u'Huko Somalia, serikali yajitetea kwa uamuzi wake wa kuhamisha \
raia kwa nguvu kutoka majengo ya serikali. mjini Mogadishu. \n',
    u'<Sync time="26.407"/>\n',
    u'Amri ya kutotoka usiku na hali ya hatari. nchini Msiri inayoendelea \
kwa muda sasa, yatikisa uchumi wa nchi hiyo. \n',
    u'</Turn>\n',
    u'<Turn speaker="spk2" startTime="34.375" endTime="66.317">\n',
    u'<Sync time="34.375"/>\n',
    u'Mimi ni Peter Musembi na kwenye michezo hapo baadaye, \
baada ya kushindwa kuvuma ligi ya. mabingwa wa Afrika, \n',
    u'<Sync time="39.933"/>\n',
    u'TP Mazembe yapania Kombe la Shirikisho? Barani Afrika. \n',
    u'<Sync time="42.813"/>\n',
    u'Mmliki wao Maurice Katumbi, asema hakuna! njia nyingine ila \
kufuzu nusu Fainali mwishoni mwa wiki. \n',
    u'<Sync time="49.264"/>\n',
    u'[music]\n',
    u'<Sync time="59.309"/>\n',
    u'[music] \n',
    u'</Turn>\n',
    u'<Turn speaker="spk1" startTime="66.317" endTime="102.008">\n',
    u'<Sync time="66.317"/>\n',
    u'[breath] Naam, hujambo na. karibu kwenye. dira ya dunia? \
dakika thelathini za habari, uchambuzi, maoni yako na michezo.\n',
    u'<Sync time="73.325"/>\n',
    u'Mimi ni Kasim Kaira, nikiwa hapa London. \n',
    u'<Sync time="76.093"/>\n',
    u'Tuanzie nchini India ambako. watu wameshangilia na kupiga! \
makofi nje ya mahakama leo hii, mjini Delhi,     \n',
    u'</Turn>\n',
    u'</Section>    \n',
]


def test_command_26(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command26(file_)

    for key in sorted(found.keys()):
        print(key, found[key])

    assert found.pop('warning_message', None) is None

    #assert 0
