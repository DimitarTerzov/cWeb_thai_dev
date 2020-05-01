# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

from utils import temporary_file
from command_4.validator_4 import command4


CONTENT = [
    u"&lt;initial&gt; error1 &lt;/initial&gt;&gt; Good evening once again.\n",            # 0
    u"<initial> error2 </initial>  And we're here to once again\n",                       # 1
    u"&lt;initial&gt; error3 &lt;initial&gt; Who have demonstrated that #uh,\n",          # 2
    u"For the &lt;initial&gt; W. E. B. &lt;/initial&gt; Du Bois.\n",                      # 3
    u"&lt;initial&gt; error4 &lt;/Initial&gt; So once again,\n",                          # 4
    u"(music) &lt;initial&gt; error5 &lt; /initial&gt;\n",                                # 5
    u"Thank you, Paul. &lt; initial&gt; error6 &lt;/initial&gt;\n",                       # 6
    u"[no-speech] &lt;initial&gt; error7 &lt;/iniial&gt;\n",                              # 7
    u"&lt;initial&gt; error8&lt;/initial&gt; My name is Julia Novena,\n",                 # 8
    u"We are going to again, uh, or George &lt;initial&gt; W. &lt;/initial&gt; Bush.\n",  # 9
    u"[noise] &lt;initial&gt;error9 &lt;/initial&gt;\n",                                  # 10
    u"Thank you. &lt;/initial&gt; error10 &lt;/initial&gt;\n",                            # 11
    u"[noise]  &lt;initial&gt; error 11 &lt;/initial&gt;\n",                              # 12
    u"[no-speech]  &lt;&lt;initial&gt; error12 &lt;/initial&gt;\n",                       # 13
    u"&lt;initial&gt; error 13 &lt;/initial &gt; In a meaningful way.\n",                 # 14
    u"It is not good enough &lt;initial&gt;error14&lt;/initial&gt; to just go\n",         # 15
    u"We must add, we must &lt;initial&gt; W! E. B. &lt;/initial&gt;\n",                  # 16
    u"The vote that we cast are &lt;initial&gt; W E B &lt;/initial&gt; important.\n",     # 17
    u"For two years, municipal, &lt;initial&gt; W?EB &lt;/initial&gt;\n",                 # 18
    u"The decision to vote always &lt;initial&gt; W! &lt;/initial&gt;\n",                 # 19
    u"This is why we &lt;initialism&gt; ČSSD &lt;/initialism&gt;\n",                       # 20
    u"between the &lt;initial&gt; PTO &lt;/initial&gt;'s\n",                              # 21
    u"by the &lt;initial&gt; พีบีเอส &lt;/initial&gt; and\n",                                 # 22
    u"Pre &lt;initial&gt; K &lt;/initial&gt; through twelveth grade.\n",                  # 23
    u"&lt;initial&gt; ซ๊เอ็นเอ็น &lt;/initial&gt;, I was a student\n",                           # 24
    u"&lt;initial&gt; PTO &lt;/initial&gt;s for the enrichment\n",                        # 25
    u"I attended &lt;initial&gt; แอลพีจีเอ &lt;/initial&gt;.\n",                                # 26
    u"I attended &lt;initial&gt; ČSSD, ČSSD &lt;/initial&gt;.\n",                           # 27
    u"French l'&lt;initial&gt; ONU &lt;/initial&gt;\n",                                   # 28
    u"This one is correct... &lt;initial&gt; Ph.D. &lt;/initial&gt;\n"                    # 29
    u"between the &lt;initial&gt; PTO &lt;/initial&gt;o\n",                               # 30
    u'&lt;initial&gt; AY &lt;/initial&gt;-liikkeen\n',                                    # 31
    u'&lt;initial&gt; AY &lt;/initial&gt;!liikkeen\n',                                    # 32
    u'&lt;initial&gt; AY &lt;/initial&gt;?liikkeen\n',                                    # 33
    u'&lt;initial&gt; AY &lt;/initial&gt;:liikkeen\n',                                    # 34
    u'&lt;initial&gt; AY &lt;/initial&gt;;liikkeen\n',                                    # 35
    u'&lt;initial&gt; AY &lt;/initial&gt;_liikkeen\n',                                    # 36
    u'&lt;initial&gt; AY &lt;/initial&gt;—liikkeen\n',                                   # 37
    u'Ремонтират улица <initial>Богориди<initial>.\n',                       # 38
    u'&lt;initial&gt; AY &lt;/initial&gt;~ \n',                                                  # 39
    u"French &lt;initial&gt; ONU &lt;/initial&gt;n\n",                               # 40
    u"French &lt;initial&gt; ONU &lt;/initial&gt;sn\n",                               # 41
    u'&lt;initial&gt;\n',                                                                                 # 42
    u'mais plutôt en termes &lt;/initial&gt;\n',                                            # 43
]
EXCLUDE = [
    1, 3, 9, 22, 23, 24,
    26, 29, 31, 32, 33, 34,
    35, 36, 37, 38, 39
]
CATCH = [
    0, 2, 4, 5, 6, 7, 8, 10,
    11, 12, 13, 14, 15, 16,
    17, 18, 19, 20, 21, 25, 27,
    28, 30, 40, 41, 42, 43
]


def test_command4(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command4(file_)

    keys = sorted(found.keys())
    print(len(keys))
    for key in keys:
        print(key, found[key])

    for row in EXCLUDE:
        assert row not in found

    for row in CATCH:
        assert row in found

    #assert 0
