# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import io


def command20(filepath):
    disallowed_punctuation = re.compile(ur"<.*?>", re.UNICODE)

    found = {}
    with io.open (filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            line = line.rstrip(' \r\n')

            if line.startswith(u'<') and line.endswith(u'>'):
                ln += 1
                continue

            match = re.search(disallowed_punctuation, line)
            if match is not  None:
                found[ln] = [20, 'Disallowed punctuation', match.group().encode('utf')]

            ln += 1

    return found


if __name__ == '__main__':
    found = command20('../files/RNZ_Insight_002.trs')
    for key in sorted(found.keys()):
        print(key, found[key])
