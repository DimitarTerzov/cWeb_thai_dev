# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import io


LANGUAGE_CODES = {
    u'bul': u'Bulgarian',
    u'eng': u'English',
    u'ell': u'Greek'
}


# Transcribers ID checker
def command0(filepath):
    transcriber_pattern = re.compile(ur'\s*<\s*Trans\s*scribe\s*=\s*"(?P<id>.*?)"', re.UNICODE)
    transcriber_id_pattern = re.compile(ur'^\w+?\-\d\d\d$', re.UNICODE)

    found = {}
    with io.open(filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            line = line.rstrip('\r\n')

            match = re.search(transcriber_pattern, line)
            if match is not None:

                transcriber_id = match.group('id').strip()
                content = transcriber_id.encode('utf')
                if  re.search(transcriber_id_pattern, transcriber_id) is not None:

                    language_code = transcriber_id[:-4]
                    if language_code in LANGUAGE_CODES:
                        found['transcriber_id'] = content
                    else:
                        found[ln] = [0, 'Incorrect Transcriber ID', content]

                else:
                    found[ln] = [0, 'Incorrect Transcriber ID', content]

                break

            ln += 1

    return found


if __name__ == '__main__':
    found = command0('')
