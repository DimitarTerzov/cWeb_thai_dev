# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import io


#Short turns
def command17(filepath):

    regex = re.compile(ur'<Sync time="\s*([0-9\.]+)\s*"/>', re.UNICODE)

    found = {}
    cur_time = None

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")
            for m in re.findall(regex, line):

                seg_time = float(m)
                if cur_time is not None:
                    seg_len = seg_time - cur_time

                    if seg_len < 3.0:
                        found[last_seq_row] = [17, 'Segment is less than 3 seconds, possible use of [overlap] or combine with other segment', 'Sync time="' + str(cur_time) + '" length: ' + str(seg_len) + ' seconds']

                #update current time
                cur_time = seg_time
                last_seq_row = ln

    return found


if __name__ == '__main__':
    found = command17('../files/test_13.trs')
    for key in sorted(found.keys()):
        print(key, found[key])
        