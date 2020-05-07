# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import io


#Numeral hunter
def command6(filepath):

    found = {}

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip(" \r\n")

            #if line starts with < and ends in >
            if line.startswith('<') and line.endswith('>'):
                #we skip everythin between <>
                continue

            words = re.findall(ur'\b\w+\b', line, re.UNICODE)
            for word in words:

                if re.match(ur'\S*\d+\S*', word, re.UNICODE) and not (word.startswith('<') and word.endswith('>')):

                    index = words.index(word)
                    if index > 0:
                        content = u'{} {}'.format(words[index - 1], word).encode('utf')
                    elif index == 0 and len(words) > 1:
                        content = u'{} {}'.format(word, words[1]).encode('utf')
                    else:
                        content = u'{}'.format(word).encode('utf')

                    found[ln] = [6, 'Numerals not allowed', content]

    return found


if __name__ == '__main__':
    found = command6('../files/AsiaWaveNews_01_sample_chawankorn.trs')

    for key in sorted(found.keys()):
        print(key, found[key])
        print(found[key][2])
