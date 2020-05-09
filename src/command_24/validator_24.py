# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import io


# Sequential turns by same speaker
def command24(filepath):

    speaker_re = re.compile(ur'spk\s*[0-9]+', re.UNICODE)
    start_time_re = re.compile(ur'startTime\s*=\s*"\s*(?P<value>[\d.]+?)\s*"', re.UNICODE)

    found = {}
    prev_spk = None
    with io.open(filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            ln += 1
            line = line.rstrip('\r\n')

            if '<Turn' in line:
                start_time_match = re.search(start_time_re, line)
                start_value = float(start_time_match.group('value').strip())
                m = re.search(speaker_re, line)
                if m is None:
                    speaker = None
                else:
                    speaker = m.group()
                    speaker = speaker.replace(' ', '')
                    if speaker == prev_spk:
                        report = '{} at {}'.format(speaker, start_value).encode('utf')
                        found[ln] = [24, 'Sequential turns by the same speaker', report]

                #save speaker
                prev_spk = speaker

    return found
