# -*- coding: utf-8 -*-
from __future__ import print_function

from utils import temporary_file
from command_5.validator_5 import command5


CONTENT = [
    u'<Turn startTime="3082.959" endTime="3084.519">\n', # 0
    u'<Sync time="3082.959"/>\n', # 1
    u'[applause] &lt;lang:Enlish&gt; ČSSD language 1 &lt;/lang:English&gt;\n', # 2
    u'</Turn>\n', # 3
    u'<Turn startTime="3086.814" endTime="3087.707">\n', # 4
    u'<Sync time="3086.814"/>\n', # 5
    u'[applause] &lt;lang:Foreign&gt; ČSSD capitalization 2 &lt;/Lang:Foreign&gt;\n', # 6
    u'<Sync time="3093.168"/>\n', # 7
    u'[noise] &lt;lang:Foreign&gt; ČSSD capitalization 3 &lt;/lang:foreign&gt;\n', # 8
    u'<Sync time="3131.57"/>\n', # 9
    u'There is ม่ทราบว่าลูกค้าสนใจ&lt;lang:Foreign&gt; Четвърти обвинен за нелегалната фабрика за \
    цигари, ม่ทราบว่าลูกค้าสนใจ &lt;/lang:Foreign&gt; ม่ทราบว่าลูกค้าสนใจ nothing like a one on one \
    conversation over coffee and a bagel to really connect with the details on issues that matter to you.\n', # 10
    u'<Sync time="3148.785"/>\n', # 11
    u'[noise]  &lt;lang:Foreign&gt;ČSSD(()) spacing 4a &lt;/lang:Foreign&gt;\n', #  12
    u'<Sync time="3150.738"/>\n', # 13
    u'&lt;lang:Foreign&gt; spacing 4b ČSSD(())&lt;/lang:Foreign&gt; Upon taking office,\n', # 14
    u'<Sync time="3170.236"/>\n', # 15
    u'[noise] &lt;lang:Foreign&gt;ČSSDspacing 5ČSSD &lt;/lang:Foreign&gt;\n', # 16
    u'<Sync time="3171.857"/>\n', # 17
    u'&lt;lang: Foreign&gt; ČSSD tag spacing 6 &lt;/lang:Foreign&gt;\n', # 18
    u'<Sync time="3184.345"/>\n', # 19
    u'These &lt;lang:Foreign&gt; Четвърти обвинен за нелегалната фабрика за цигари, \
    ม่ทราบว่าลูกค้าสนใจ &lt;/lang:Foreign&gt;ม่ทราบว่าลูกค้าสนใจ\n', # 20
    u'<Sync time="3197.754"/>\n', # 21
    u'&lt;lang:Foreign&gt; ČSSD missing slash 7 &lt;lang:Foreign&gt;I grew up hungry\n', # 22
    u'<Sync time="3207.962"/>\n', # 23
    u"&lt; lang:Foreign&gt; ČSSD tag spacing 8 &lt;/lang:Foreign&gt; We've also\n", # 24
    u'<Sync time="3213.568"/>\n', # 25
    u'[lipsmack] <lang:Spanish> ČSSD wrong tags in code error 9 </lang:Spanish> Over\n', # 26
    u'<Sync time="3224.352"/>\n', # 27
    u'&lt;lang:Foreign&gt;&gt; double > error 10 ČSSD  &lt;/lang:Foreign&gt; [lipsmack]\n', # 28
    u'<Sync time="3234.082"/>\n', # 29
    u'&lt;lang:Foreign&gt; error 11 ČSSD. &lt;/lang:Foreign&gt; [breath]\n', # 30
    u'</Turn>\n', # 31
    u'<Turn startTime="3362.063" endTime="3364.044">\n', # 32
    u'<Sync time="3246.403"/>\n', # 33
    u'Afterschool waitlists &lt;lang:English&gt;  &lt;/lang:English&gt;\n', # 34
    u'<Sync time="3270.24"/>\n', # 35
    u'The first step &lt;lang:English&gt; to ČSSD that is a, feasibility, study—  &lt;/lang:English&gt; to that\n', # 36
    u'<Sync time="3336.788"/>\n', # 37
    u'There &lt;lang:English&gt; word, word (()) <initial> ČSSD <initial>, etc. &lt;/lang:English&gt;\n', # 38
    u'<Sync time="3349.75"/>\n', # 39
    u"It is your &lt;lang:English&gt; ČSSD perspective &lt;lang:English&gt; lang tag inside lang \
tag &lt;/lang:English&gt; ČSSD and voice &lt;/lang:English&gt; perspective\n", # 40
    u'<Sync time="379.522"/>\n', # 41
    u'&lt;lang:Portuguese&gt;\n', # 42
    u'<Sync time="411.39"/>\n', # 43
    u"เมื่อเจาะจงต่อกรรที่วิสาหกิจขนาดกลาง ขนาดเล็ก &lt;/lang: Portuguese&gt; \
และขนาดย่อม ทั้งหลายต่างได้รับผลกระทบจากโรคระบาดครั้งนี้\n", # 44
    u'<Sync time="411.39"/>\n', # 45
    u'ให้การสนับ สนุนก &lt;lang:Portuguese&gt; ารสร้างควา มมั่นคงแก่พนักงานในองค์การ\n',    # 46
    u'</Turn>\n', # 47
]

EXCLUDE = [
    0, 1, 3, 4, 5, 7, 9, 11, 13, 15,
    17, 19, 21, 23, 25, 26, 27, 29,
    31, 32, 33, 35, 37, 38, 39, 41,
    43, 45, 47
]

CATCH = [
    2, 6, 8, 10, 12, 14, 16, 18, 20,
    22, 24, 28, 30, 34, 36, 40, 42,
    44, 46
]


def test_command5(tmpdir):
    file_ = temporary_file(tmpdir, CONTENT)
    found = command5(file_)

    for key in sorted(found.keys()):
        print(key, found[key])


    for row in EXCLUDE:
        assert row not in found

    for row in CATCH:
        assert row in found

    #assert 0
