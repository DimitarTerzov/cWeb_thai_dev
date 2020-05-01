from __future__ import print_function

import re
import io


def command23(filepath):
    bad_strings_to_report = {
        u'Who nb=': u'Do not create turns with multiple speakers.',
        u'Topic id=': u'Do not create topics',
        u'Event desc=': u'Do not create events',
        u'mode=': u'Do not change the mode setting',
        u'channel=': u'Do not change the channel setting',
        u'fidelity=': u'Do not change the fidelity setting',
        u'Background time=': u'Disallowed use of Transcriber',
        u'Comment desc=': u'Disallowed use of Transcriber'
    }
    found = {}
    regex = re.compile(ur".*<(.*)>.*", re.UNICODE)
    in_section = False

    with io.open (filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip('\r\n')

            if re.search(ur'<\s*Section', line, re.UNICODE) is not None:
                in_section = True
            elif re.search(ur'<\s*/\s*Section', line, re.UNICODE) is not None:
                in_section = False

            if in_section:
                inner = re.findall(regex, line)
                # < inner >
                for txt in inner:

                    for bad in bad_strings_to_report:
                        if bad in txt:
                            report_line = u'({}) | {})'.format(bad, line).encode('utf')
                            found[ln] = [23, bad_strings_to_report[bad].encode('utf'), report_line]

    return found


if __name__ == '__main__':
    found = command23('../files/P3_News_2020_01_13_1_part2.trs')
    for key in sorted(found.keys()):
        print(key, found[key])
