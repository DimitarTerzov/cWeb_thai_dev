# -*- coding: utf-8 -*-
import re
import io


#Filler word validator
def command7(filepath):

    # Allowed punctuation after tag
    punctuation = u"[:',!—_\".?\-;]"
    #default skip tags
    skip_tags = u'(#อือ|#อืม|#เอ่อ|#อ่า|#เออ|#ฮืม)'
    filler_re = re.compile(ur'[\W\w]?#\w[\s\w][\s\w]\w?\W?', re.UNICODE)

    found = {}
    in_section = False
    tag_exists = False
    with io.open(filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            ln += 1
            line = line.rstrip("\r\n")

            if '<Section' in line:
                in_section = True
            elif '</Section' in line:
                in_section = False

            for match in re.finditer(filler_re, line):
                tag_exists = True

                target = match.group().strip()
                # Pass filler tag with tilde.
                # They are reported in command 15.
                if "~" in target:
                    continue

                if (
                    not re.match(ur'^{0}{1}?$'.format(skip_tags, punctuation), target, re.UNICODE)
                    and in_section
                ):
                    found[ln] = [7, 'Invalid filler tag', target.encode('utf')]

    if not tag_exists:
        found['warning_message'] = 'No fillers tags were found. Please refer to the project \
page to learn about the required use of filler tags.'

    return found


if __name__ == '__main__':
    found = command7("../files/AsiaWaveNews_13.trs")
    keys = sorted(found.keys())
    for key in keys:
        print key, found[key], found[key][2]
