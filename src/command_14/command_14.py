# -*- coding: utf-8 -*-
from __future__ import print_function

import io
import re

#Segment length validator
def command14(filepath):

    regex = re.compile(ur'<Sync\s*time\s*=\s*"\s*([0-9\.]+)\s*"\s*/>')

    found = {}
    cur_time = 0

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = 1
        for line in f:
            line = line.rstrip("\r\n")
            for m in re.findall(regex, line):

                seg_time = float(m)
                seg_len = seg_time - cur_time

                if seg_len > 15.0:
                    found[ln] = [14, 'Segment exceeds limit', 'Sync time="{}"; length: {} seconds'.format(seg_time, seg_len)]

                #update current time
                cur_time = seg_time

            ln += 1

    return found


if __name__ == '__main__':
    found = command14('../files/RNZ_Insight_002.trs')
    for key in sorted(found.keys()):
        print(key, found[key])
