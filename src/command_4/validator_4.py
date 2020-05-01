# -*- coding: utf-8 -*-
import re
import io

from command_5.validator_5 import _prepare_content


#Initial tag validator
def command4(filepath):

    punctuation = u"""[^_.,!?\s:;—"\-~]"""
    # To add new accent extend the list
    # followind the pattern
    accents = [u'๊', u'ี', u'็']
    accents = u''.join(accents)
    # Add characters to the list like:
    # allowed_characters_after_tag = [u"s", u"n"]
    #allowed_expressions_before_tag = [u"l'", u"O'"]
    allowed_characters_after_tag = [u""]
    allowed_expressions_before_tag = [u""]
    regex = re.compile(ur"(?P<content>(?P<before_first>(\b\w*\b)|[\S\w]+)?&lt;(?P<first_tag>[int\w\s/\\]+)&gt;(?P<inner_text>.*?)&lt;(?P<forward>[\\/\s]*)(?P<second_tag>[int\w\s]+)&gt;(?P<after_second>\b\w*\b|{}+)?)".format(punctuation), re.UNICODE)
    opening_tag = re.compile(ur'&lt;[int\w\s]+&gt;', re.UNICODE)
    closing_tag = re.compile(ur'&lt;\s*/[int\w\s]+&gt;', re.UNICODE)

    found = {}
    tag_exists = False
    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip('\r\n')

            if (
                re.search(opening_tag, line) is not None and
                re.search(closing_tag, line) is None
            ):
                open_tag = re.search(opening_tag, line).group(0)
                content = _prepare_content(open_tag)
                found[ln] = [4, "Missing closing tag", content]
                tag_exists = True

            if (
                re.search(opening_tag, line) is None and
                re.search(closing_tag, line) is not None
            ):
                close_tag = re.search(closing_tag, line).group(0)
                content = _prepare_content(close_tag)
                found[ln] = [4, "Missing opening tag", content]
                tag_exists = True

            for m in re.finditer(regex, line):
                tag_exists = True
                error_tag = m.group('content')
                error_tag = _prepare_content(error_tag)

                # Check tag syntax
                if m.group('forward') != u'/':
                    found[ln] = [4, 'Initial tag error', error_tag]
                    continue

                # Check tag spelling
                if (
                    m.group('first_tag') != 'initial' or
                    m.group('second_tag') != 'initial'
                ):
                    found[ln] = [4, 'Initial tag error', error_tag]
                    continue

                # Check for disallowed expressions before tag
                if (
                    m.group('before_first') is not None and
                    not m.group('before_first') in allowed_expressions_before_tag
                ):
                    found[ln] = [4, 'Initial tag error', error_tag]
                    continue

                # Check for disallowed expressions after tag
                if (
                    m.group('after_second') is not None and
                    not m.group('after_second') in allowed_characters_after_tag and
                    not m.group('after_second').startswith(u'_')
                ):
                    found[ln] = [4, 'Initial tag error', error_tag]
                    continue

                # Check for incorrect white space
                if (
                    not m.group('inner_text').startswith(' ') or
                    not m.group('inner_text').endswith(' ')
                ):
                    found[ln] = [4, 'Initial tag error', error_tag]
                    continue

                # Check for errors in text
                inner_text = m.group('inner_text')
                inner_content = inner_text.split()
                # If no text in tag -> error
                if not inner_content:
                    found[ln] = [4, 'Initial tag error', error_tag]

                elif len(inner_content) == 1:
                    content = inner_content[0]
                    # Catch anything different from pattern `W`
                    if len(content) == 1 and re.match(ur'\W', content, re.UNICODE):
                        found[ln] = [4, 'Initial tag error', error_tag]

                    # Catch anything different from pattern `WE` and `W.`
                    elif len(content) == 2 and not re.match(ur'^\w+\.?$', content, re.UNICODE):
                        found[ln] = [4, 'Initial tag error', error_tag]

                    # Catch anything different from pattern `WEB`, `Ph.D.`
                    elif len(content) > 2:
                        if re.match(ur'[\w.{}]*'.format(accents), content, re.UNICODE).group() != content:
                            found[ln] = [4, 'Initial tag error', error_tag]

                # If text doesn't feet pattern `W. E. B.` -> error
                elif len(inner_content) > 1:
                    for content in inner_content:
                        if not re.match(ur'^\w[{}]?\.$'.format(accents), content, re.UNICODE):
                            found[ln] = [4, 'Initial tag error', error_tag]

    if not tag_exists and not found:
        found[1] = [4, 'Be sure to include initial tag for any and all initialisms. If there were no initialisms, feel free to ignore this error.', '']

    return found


if __name__ == '__main__':
    found = command4('../files/News_ThaiPBSEveningNews_20160518.trs')
    keys = found.keys()
    keys = sorted(keys)
    print len(keys)
    for key in keys:
        print key, found[key]
