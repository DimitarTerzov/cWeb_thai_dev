# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import io


#Disallowed characters
def command1(filepath):
    ## String: Update with new chars between the regex brackets [..] ##
    bad_chars = "[£$@}%^&*{…–—;:\"/❛❜❝❞〃״＇״‷⁗‴「」『』„”‚“”‘„”»«""‘“”«»‹›„““”‘‹›«»„（）［］｛｝｟｠⦅⦆〚〛⦃⦄「」〈〉《》【】〔〕⦗⦘『』〖〗〘〙｢｣⟦⟧⟨⟩⟪⟫⟮⟯⟬⟭⌈⌉⌊⌋⦇⦈⦉⦊❨❩❪❫❴❵❬❭❮❯❰❱❲❳﴾﴿〈〉⦑⦒⧼⧽﹙﹚﹛﹜﹝﹞⁽⁾₍₎⦋⦌⦍⦎⦏⦐⁅⁆⸢⸣⸤⸥⟅⟆⦓⦔⦕⦖⸦⸧⸨⸩⧘⧙⧚⧛᚛᚜༺༻༼༽⸜⸝⸌⸍⸂⸃⸄⸅⸉⸊⏜⏝⎴⎵⏞⏟⏠⏡﹁ ﹂﹃﹄︹︺︻︼︗︘︿﹀︽︾﹇﹈︷︸]".decode('utf')
    ## strip off any remaining whitespace char
    s = u"".join(bad_chars.split())
    ## from utf-8 to unicode encode
    regex = s

    found = {}

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")

            #if line starts with < and ends in >
            if line.startswith('<') and line.endswith('>'):
                #we skip everythin between <>
                continue

            #remove all lt/gt from the line
            p1 = line.find('&lt;')
            p2 = line.find('&gt;')
            while p1 >= 0 and p2 > p1:
                if (p2 + 4) == len(line):
                    line = u''
                else:
                    line = line[0:p1] + line[p2+4]
                p1 = line.find('&lt;')
                p2 = line.find('&gt;')

            #uniline = unicode(line,"utf-8")

            dissch = re.findall(regex, line)
            s = u''.join(dissch)

            if len(dissch) > 1:
                found[ln] = [1, 'Disallowed characters', s.encode("utf-8") + '/' + line.encode('utf')]
            if len(dissch)==1:
                found[ln] = [1, 'Disallowed character', s.encode("utf-8") + '/' + line.encode('utf')]

    return found


if __name__ == '__main__':
    found = command1('../files/test_5.trs')
    for key in sorted(found.keys()):
        print(key, found[key])
