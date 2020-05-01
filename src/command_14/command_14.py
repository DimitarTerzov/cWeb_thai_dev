# -*- coding: utf-8 -*-
from __future__ import print_function

import io
import re

#Segment length validator
def command14(filepath):

    regex = re.compile(ur'<Sync\s*time\s*=\s*"\s*([0-9\.]+)\s*"\s*/>', re.UNICODE)
    section_end_time =re.compile(ur'<Section.*?endTime="([\d.]+)', re.UNICODE)

    found = {}
    cur_time = 0

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            line = line.rstrip("\r\n")

            if re.search(section_end_time, line) is not None:
                end_time = float(re.search(section_end_time, line).group(1))

            for m in re.findall(regex, line):
                last_sync_line = ln

                seg_time = float(m)
                seg_len = seg_time - cur_time

                if seg_len > 15.0:
                    found[ln] = [14, 'Segment exceeds limit', 'Sync time="{}"; length: {} seconds'.format(seg_time, seg_len)]

                #update current time
                cur_time = seg_time

            if u'</Section>' in line:
                seg_len = end_time - cur_time

                if seg_len > 15.0:
                    found[last_sync_line] = [14, 'Segment exceeds limit', 'Sync time="{}"; length: {} seconds'.format(cur_time, seg_len)]


            ln += 1

    return found


if __name__ == '__main__':
    found = command14('../files/RNZ_Insight_002.trs')
    for key in sorted(found.keys()):
        print(key, found[key])
