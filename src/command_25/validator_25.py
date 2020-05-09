# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import io


# Code errors
def command25(filepath):

    inspect_sync_re = re.compile(ur'<(\s*)[Sync\w]+(?:\s*)[time\w]+(\s*)=(\s*)"(\s*)[\d\.]+(\s*)"/(\s*)>', re.UNICODE)
    inspect_turn_re = re.compile(ur'<[Turn\w]+(?:\s*[speaker\w]+(\s*)=(\s*)"(\s*)[spk\w]+\d+(\s*)")?\s*[startTime\w]+(\s*)=(\s*)"(\s*)[\d\.]+(\s*)"\s*[endTime\w]+(\s*)=(\s*)"(\s*)[\d\.]+(\s*)"(?:\s*[speaker\w]+(\s*)=(\s*)"(\s*)[spk\w]+\d+(\s*)")?>', re.UNICODE)
    closing_turn = re.compile(ur'\s*<\s*/\s*Turn\s*>', re.UNICODE)

    found = {}
    with io.open(filepath, 'r', encoding='utf') as f:

        ln = 0
        sync = False
        empty_row = None
        not_empty_row = False
        for line in f:
            ln += 1
            line = line.rstrip("\r\n")

            match = re.match(inspect_sync_re, line)
            if match is not None:
                if empty_row is not None and not_empty_row:
                    found[empty_row] = [25, 'Empty row in Sync tag', '']
                sync = True
                empty_row = None
                not_empty_row = False

                if re.search(ur'\bSync\b\s*\btime\b', line, re.UNICODE) is None:
                    found[ln] = [25, 'Tag syntax error', line.encode('utf')]
                    continue

                for group in match.groups():
                    if group is not None and group != "":
                        found[ln] = [25, 'Unexpected white space in Sync tag', line.encode('utf')]
                        break

                continue

            if sync and line and re.search(closing_turn, line) is None:
                not_empty_row = True
            elif sync and not line:
                empty_row = ln

            if re.search(closing_turn, line):
                if empty_row and not_empty_row:
                    found[empty_row] = [25, 'Empty row in Sync tag', '']
                sync = False
                empty_row = None
                not_empty_row = False

            match = re.match(inspect_turn_re, line)
            if match is not None:

                if re.search(ur'\bTurn\b.*?\bstartTime\b.*?\bendTime\b.*?>', line, re.UNICODE) is None:
                    found[ln] = [25, 'Tag syntax error', line.encode('utf')]
                    continue

                for group in match.groups():
                    if group is not None and group != "":
                        found[ln] = [25, 'Unexpected white space in Turn tag', line.encode('utf')]
                        break

                continue

            if u'<Speaker' in line and line != '<Speakers>':
                if re.match(ur'<Speaker.*?/>', line, re.UNICODE) is None:
                    found[ln] = [25, 'Tag syntax error', line.encode('utf')]

    return found


if __name__ == '__main__':
    found = command25(r'../files/Ykkosaamu_007.trs')
    print(len(found))
    keys = sorted(found.keys())
    for key in keys:
        print(key, found[key])
