# -*- coding: utf-8 -*-
import re
import io


#Tilde checker
def command15(filepath):

    punctuation = u":',!—_\".?\-;\]\["

    match_no_white_space = re.compile(ur'(\b\w+~\w*\b)', re.UNICODE)
    match_double_white_space = re.compile(ur'\w* ~ \w*', re.UNICODE)
    match_double_tilde = re.compile(ur'\w*\s*~~\s*\w*', re.UNICODE)
    match_punctuation_before = re.compile(ur"[{0}]~[{0}]?".format(punctuation), re.UNICODE)
    match_punctuation_after = re.compile(ur"(?<=\s)~[{0}]".format(punctuation), re.UNICODE)
    match_tilde_at_start = re.compile(ur'^~[{}]'.format(punctuation + u"\s"), re.UNICODE)
    match_filler = re.compile(ur"#\w*~", re.UNICODE)


    found = {}
    tag_exists = False
    in_section = False
    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1

            if u'<Section' in line:
                in_section = True

            if in_section and u'~' in line:
                tag_exists = True

            no_white_space = re.findall(match_no_white_space, line)
            for match in no_white_space:
                found[ln] = [15, 'Incorrect white space', match.encode('utf')]

            double_white_space = re.findall(match_double_white_space, line)
            for match in double_white_space:
                found[ln] = [15, 'Incorrect white space', match.encode('utf')]

            double_tilde = re.findall(match_double_tilde, line)
            for match in double_tilde:
                found[ln] = [15, 'Double tilde', match.encode('utf')]

            if re.search(match_punctuation_before, line) is not None:
                for word in line.split():
                    if u'~' in word and not word.endswith(u'&gt;~'):
                        found[ln] = [15, 'Punctuation touching tilde', word.encode('utf')]

            touching_punctuation_after = re.finditer(match_punctuation_after, line)
            for match in touching_punctuation_after:
                found[ln] = [15, 'Punctuation touching tilde', match.group().encode('utf')]

            fillers = re.finditer(match_filler, line)
            for match in fillers:
                found[ln] = [15, 'Filler word with tilde', match.group().encode('utf')]

            incorrect_tilde = re.match(match_tilde_at_start, line)
            if incorrect_tilde:
                found[ln] = [15, 'Incorrect use of tilde', incorrect_tilde.group().encode('utf')]

    if not tag_exists and not found:
        found[1] = [15, 'No tildes were found. Please refer to the project page to learn about the proper use of the tilde for partially spoken words. If there were no partially spoken words, feel free to ignore this error.', '']

    return found


if __name__ == '__main__':
    found = command15('../files/no_tags.trs')
    for row, hit in found.items():
        print row, ' => ', hit
