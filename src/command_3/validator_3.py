# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import io

from app.cWeb import WWpunctuatio, WWwhitespace


#Sound tag validator
def command3(filepath):
    skip_words = [
        u'[no-speech]', u'[no—speech]', u'[noise]',
        u'[overlap]', u'[music]', u'[applause]',
        u'[lipsmack]', u'[breath]', u'[cough]',
        u'[laugh]', u'[click]', u'[ring]',
        u'[dtmf]', u'[sta]', u'[cry]', u'[prompt]'
    ]

    regex = re.compile(ur"\[.*?\]", re.UNICODE)

    found = {}
    tag_exists = False
    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")
            prev_tag = 'none'

            if '<Speaker' not in line:

                for w in line.split():
                    # if we have something glued to tag

                    if re.match(ur".*[^ \s、 。 ‧ ？ ！ ，]\[.*?\]", w, re.UNICODE):
                        found[ln] = [3, 'Missing white space left of sound tag', w.encode('utf')]
                        tag_exists = True
                    elif re.match(ur"\[.*?\][^ \s.,，。\-?! ].*", w, re.UNICODE):
                        found[ln] = [3, 'Missing white space right of sound tag', w.encode('utf')]
                        tag_exists = True
                    else:
                        for m in re.findall(regex, line):
                            if not m in skip_words:
                                found[ln] = [3, 'Sound tag syntax', '{}/{}'.format(m.encode('utf'), line.encode('utf'))]

                            # detect duplicate tags like - [cough] [cough]
                            # if we have two of the same tags in a row
                            # and they are one by one in the line
                            elif prev_tag == m and re.search(ur'{0}\s*{1}*{2}*{3}'.format(re.escape(m), WWwhitespace.decode('utf'), WWpunctuatio.decode('utf'),   re.escape(m)), line, re.UNICODE) is not None:
                                found[ln] = [3, 'Sound tag duplicate', '{}/{}'.format(m.encode('utf'), line.encode('utf'))]
                            prev_tag = m
                            tag_exists = True

    if not tag_exists and not found:
        found[1] = [3, 'No sound tag were found. Please refer to the project page to learn about the required use of sound tags.', '']

    return found


if __name__ == '__main__':
    found = command3('../files/CT_Newsevents_34.trs')
    for key in sorted(found.keys()):
        print(key, found[key])

