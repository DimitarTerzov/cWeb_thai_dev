# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import io


#Turn validator
def command13(filepath):

    found = {}
    sync = False
    sync_count = 0
    end_time = 0
    sync_line = None
    with io.open(filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            ln += 1
            line = line.rstrip('\r\n')

            if '<Turn' in line:
                start_time_match = re.search(ur'(?P<content>startTime\s*=\s*"\s*(?P<value>[\d.]+?)\s*")', line, re.UNICODE)
                start_value = float(start_time_match.group('value').strip())
                start_time = start_time_match.group('content')

                # Catch turns out of order
                if start_value != end_time:
                    found[ln] = [13, "Turn out of sync", start_time.encode('utf')]

                end_time = re.search(ur'endTime\s*=\s*"\s*(?P<value>[\d.]+?)\s*"', line, re.UNICODE)
                end_time = float(end_time.group('value').strip())

                if start_value >= end_time:
                    found[ln] = [13, "Turn out of sync", start_time.encode('utf')]

                sync_count = 0

            elif line.startswith('<Sync') and not sync:
                sync_line = ln
                sync = True
                sync_count += 1
                new_sync = re.search(ur'(?P<content>Sync\s*time\s*=\s*"\s*(?P<value>[\d.]+?)\s*")', line, re.UNICODE)
                new_sync_time = new_sync.group('content')
                sync_time_value = float(new_sync.group('value').strip())

                if sync_count == 1:
                    # compare sync_time with start_value
                    if sync_time_value != start_value:
                        found[ln] = [13, "Segment out of sync", new_sync_time.encode('utf')]

                elif sync_count > 1:
                    # compare new sync_time with old sync_time
                    old_sync_value = re.search(ur'([\d.]+)', sync_time)
                    if (
                        sync_time_value <= float(old_sync_value.group()) or
                        sync_time_value > end_time
                    ):
                        found[ln] = [13, "Segment out of sync", new_sync_time.encode('utf')]

                sync_time = new_sync_time

            elif "</Turn>" == line and sync and sync_count == 1:
                found[sync_line] = [13, "Empty segments are not allowed", sync_time.encode('utf')]
                sync = False
                sync_count = 0

            elif line.startswith('<Sync') and sync:
                found[sync_line] = [13, "Empty segments are not allowed", sync_time.encode('utf')]
                sync_count += 1
                new_sync = re.search(ur'(?P<content>Sync\s*time=\s*"\s*(?P<value>[\d.]+?)\s*")', line, re.UNICODE)
                sync_time = new_sync.group('content')
                sync_line = ln

            elif not line.startswith('<Sync') and line != "</Turn>":
                if line != '':
                    sync = False

            elif "</Turn>" == line and sync and sync_count > 1:
                found[sync_line] = [13, "Empty segments are not allowed", sync_time.encode('utf')]
                sync = False
                sync_count = 0

            elif "</Turn>" == line and not sync:
                sync = False
                sync_count = 0

    return found


if __name__ == "__main__":

    found = command13('../files/CT_Newsevents_40.trs')
    for key in sorted(found.keys()):
        print(key, found[key])
