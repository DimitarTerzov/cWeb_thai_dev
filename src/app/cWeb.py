#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = '1.29'
import os
import sys
import re
import datetime
import cgi, cgitb
import binascii
import io
cgitb.enable()


DISABLE_COMMANDS = {
    0: True, 1: False, 2: False, 3: False, 4: False,
    5: False, 6: False, 7: False, 8: False, 9: False,
    10: False, 11: False, 12: False, 13: False, 14: False,
    15: False, 16: False, 17: False, 18: False, 19: False,
    20: False, 21: False, 22: False, 23: False, 24: False,
    25: False
}
LANGUAGE_CODES = {
    u'bul': u'Bulgarian',
    u'eng': u'English',
    u'ell': u'Greek'
}

# To add new accent extend the list
# followind the pattern
accents = [u'๊', u'ี', u'็', u'่', u'ั', u'ู้', u'ุ', u'ิ่']
ACCENTS = u''.join(accents)

# Extracted from: https://www.tamasoft.co.jp/en/general-info/unicode.html
WWwhitespace = "[\s                                                                                                      ฀឴   ឵᠋  ᠌   ᠍   ᠎   ᠏᠚  ᠛   ᠜   ᠝   ᠞   ᠟ᡸ  ᡹   ᡺   ᡻   ᡼   ᡽   ᡾   ᡿ᢪ  ᢫   ᢬   ᢭   ᢮   ᢯                                           ​   ‌   ‍   ‎   ‏                            ⁠  ⁡   ⁢   ⁣   ⁤   ⁥   ⁦   ⁧   ⁨   ⁩   ⁪   ⁫   ⁬   ⁭   ⁮   ⁯⠀　꒍    ꒎   ꒏꒢  ꒣꓅﬏︀    ︁   ︂   ︃   ︄   ︅   ︆   ︇   ︈   ︉   ︊   ︋   ︌   ︍   ︎   ️￰  ￱   ￲   ￳   ￴   ￵   ￶   ￷   ￸   ￹   ￺   ￻   ]"
# Extracted from: https://www.fileformat.info/info/unicode/category/Po/list.htm
# ᳀᳁᳂᳃᳄᳅᳆᳇᳓৽੶౷಄࿙࿚⸱⸲⸳⸴⸵⸶⸷⸸⸹⸼⸽⸾⸿⹁⹃⹄⹅⹆⹇⹈⹉⹊⹋⹌⹍⹎⹏꣸꣹꣺꣼𐫰𐫱𐫲𐫳𐫴𐫵𐫶𐮙𐮚𐮛𐮜𐽕𐽖𐽗𐽘𐽙𒑴𖩮𖩯𖫵𖬷𖬸𖬹𖬺𖬻𖭄𖺗𖺘𖺙𖺚𖿢𛲟𝪇𝪈𝪉𝪊𝪋𞥞𞥟𑗎𑗏𑗐𑗑𑗒𑗓𑗔𑗕𑗖𑗗𑙁𑙂𑙃𑙠𑙡𑙢𑙣𑙤𑙥𑙦𑙧𑙨𑙩𑙪𑙫𑙬𑜼𑜽𑜾𑠻𑧢𑨿𑩀𑩁𑩂𑩃𑩄𑩅𑩆𑪚𑪛𑪜𑪞𑪟𑪠𑪡𑪢𑱁𑱂𑱃𑱄𑱅𑱰𑱱𑻷𑻸𑿿𑅀𑅁𑅂𑅃𑅴𑅵𑇅𑇆𑇇𑇈𑇍𑇛𑇝𑇞𑇟𑈸𑈹𑈺𑈻𑈼𑈽𑊩𑑋𑑌𑑍𑑎𑑏𑑛𑑝𑓆𑗁𑗂𑗃𑗄𑗅𑗆𑗇𑗈𑗉𑗊𑗋𑗌𑗍
WWpunctuatio = "[\!\"\#\'\%\*\,\.\:\?\@\¡§¶·¿;·՚՛՜՝՞։׀׃׆׳״؉؊،؍؛؞؟٪٫٬٭۔܀܁܂܃܄܅܆܇܈܉܊܋܌܍߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾࡞।॥॰૰෴๏๚๛༄༅༆༇༈༉༊་༌།༎༏༐༑༒༔྅࿐࿑࿒࿓࿔၊။၌၍၎၏჻፠፡።፣፤፥፦፧፨᙮᛫᛬᛭᜵᜶។៕៖៘៙៚᠀᠁᠂᠃᠄᠅᠇᠈᠉᠊᥄᥅᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᯼᯽᯾᯿᰻᰼᰽᰾᰿᱾᱿‖‗†‡•‣․‥…‧‰‱′″‴‵‶‷‸※‼‽‾⁁⁂⁃⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁓⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⳹⳺⳻⳼⳾⳿⵰⸀⸁⸆⸇⸈⸋⸎⸏⸐⸑⸒⸓⸔⸕⸖⸘⸛⸞⸟⸪⸫⸬⸭⸮⸰、。〃〽・꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷꡴꡵꡶꡷꣎꣏꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꫞꫟꫰꫱꯫︐︑︒︓︔︕︖︙︰﹅﹆﹉﹊﹋﹌﹐﹑﹒﹔﹕﹖﹗﹟﹠﹡﹨﹪﹫！＂＃％＆＇＊，．／：；？＠＼｡､･𐄀𐄁𐄂𐎟𐏐𐡗𐤟𐤿𐩐𐩑𐩒𐩓𐩔𐩕𐩖𐩗𐩘𐩿𐬹𐬺𐬻𐬼𐬽𐬾𐬿𑁇𑁈𑁉𑁊𑁋𑁌𑁍𑂻𑂼𑂾𑂿𑃀𑃁𒑰𒑱𒑲𒑳᳀᳁᳂᳃᳄᳅᳆᳇᳓৽੶౷಄࿙࿚⸱⸲⸳⸴⸵⸶⸷⸸⸹⸼⸽⸾⸿⹁⹃⹄⹅⹆⹇⹈⹉⹊⹋⹌⹍⹎⹏꣸꣹꣺꣼𐫰𐫱𐫲𐫳𐫴𐫵𐫶𐮙𐮚𐮛𐮜𐽕𐽖𐽗𐽘𐽙𒑴𖩮𖩯𖫵𖬷𖬸𖬹𖬺𖬻𖭄𖺗𖺘𖺙𖺚𖿢𛲟𝪇𝪈𝪉𝪊𝪋𞥞𞥟𑗎𑗏𑗐𑗑𑗒𑗓𑗔𑗕𑗖𑗗𑙁𑙂𑙃𑙠𑙡𑙢𑙣𑙤𑙥𑙦𑙧𑙨𑙩𑙪𑙫𑙬𑜼𑜽𑜾𑠻𑧢𑨿𑩀𑩁𑩂𑩃𑩄𑩅𑩆𑪚𑪛𑪜𑪞𑪟𑪠𑪡𑪢𑱁𑱂𑱃𑱄𑱅𑱰𑱱𑻷𑻸𑿿𑅀𑅁𑅂𑅃𑅴𑅵𑇅𑇆𑇇𑇈𑇍𑇛𑇝𑇞𑇟𑈸𑈹𑈺𑈻𑈼𑈽𑊩𑑋𑑌𑑍𑑎𑑏𑑛𑑝𑓆𑗁𑗂𑗃𑗄𑗅𑗆𑗇𑗈𑗉𑗊𑗋𑗌𑗍]"
# for command3 and command10
BasicPunctuation = "[.,，。\-?! ]"

def build_sync_times(filepath):
    sync_t = {}

    last_sync = u""

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1

            line = line.rstrip("\r\n")
            if re.match(ur"<Sync time=\"[\s\d\.]+\"/>", line, re.UNICODE):
                last_sync = line

            sync_t[ln] = last_sync.encode('utf')

    return sync_t


def build_audio_times(sync_times):
    audio_times = {}

    for key, value in sync_times.iteritems():
        if value:
            audio_times[key] = get_audio_time(value)
        else:
            audio_times[key] = value

    return audio_times


def get_audio_time(sync_time):
    time = re.search(r'\d+', sync_time).group()
    return str(datetime.timedelta(seconds=int(time)))


def list_files(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.trs' in file:
                files.append(os.path.join(r, file))
    return files


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


#Bracket hunter
def command2(filepath):
    found = {}
    with open(filepath,'r') as f:

        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")

            #if line starts with < and ends in >
            if line.startswith('<') and line.endswith('>'):
                #we skip everythin between <>
                continue

            orig_line = line

            #exclude [*]
            for m in re.findall("(\[[^\]]*\])", line):
                line = line.replace(m, '')

            #if the word contains a bracket, after all [*] tags where removed
            if re.search('\[|\]', line):
                found[ln] = [2, 'Bracket issue [', orig_line]
    return found


#Sound tag validator
def command3(filepath):
    skip_words = [
        u'[no-speech]', u'[no—speech]', u'[noise]',
        u'[overlap]', u'[music]', u'[applause]',
        u'[lipsmack]', u'[breath]', u'[cough]',
        u'[laugh]', u'[click]', u'[ring]',
        u'[dtmf]', u'[sta]', u'[cry]', u'[prompt]'
    ]

    regex = re.compile(ur"\[.*?\]", re.UNICODE)

    found = {}
    tag_exists = False
    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")
            prev_tag = 'none'

            if '<Speaker' not in line:

                for w in line.split():
                    # if we have something glued to tag

                    if re.match(ur".*[^ \s、 。 ‧ ？ ！ ，]\[.*?\]", w, re.UNICODE):
                        found[ln] = [3, 'Missing white space left of sound tag', w.encode('utf')]
                        tag_exists = True
                    elif re.match(ur"\[.*?\][^ \s.,，。\-?! ].*", w, re.UNICODE):
                        found[ln] = [3, 'Missing white space right of sound tag', w.encode('utf')]
                        tag_exists = True
                    else:
                        for m in re.findall(regex, line):
                            if not m in skip_words:
                                found[ln] = [3, 'Sound tag syntax', '{}/{}'.format(m.encode('utf'), line.encode('utf'))]

                            # detect duplicate tags like - [cough] [cough]
                            # if we have two of the same tags in a row
                            # and they are one by one in the line
                            elif prev_tag == m and re.search(ur'{0}\s*{1}*{2}*{3}'.format(re.escape(m), WWwhitespace.decode('utf'), WWpunctuatio.decode('utf'),   re.escape(m)), line, re.UNICODE) is not None:
                                found[ln] = [3, 'Sound tag duplicate', '{}/{}'.format(m.encode('utf'), line.encode('utf'))]
                            prev_tag = m
                            tag_exists = True

    if not tag_exists and not found:
        found[1] = [3, 'No sound tag were found. Please refer to the project page to learn about the required use of sound tags.', '']

    return found


#Initial tag validator
def command4(filepath):

    punctuation = u"""_.,!?:;—"\-~"""

    # Add characters to the list like:
    # allowed_characters_after_tag = [u"s", u"n"]
    #allowed_expressions_before_tag = [u"l'", u"O'"]
    allowed_characters_after_tag = [u""]
    allowed_expressions_before_tag = [u""]
    regex = re.compile(ur"(?P<content>(?P<before_first>(\b\w*\b)|[\S\w]+)?&lt;(?P<first_tag>[int\w\s/\\]+)&gt;(?P<inner_text>.*?)&lt;(?P<forward>[\\/\s]*)(?P<second_tag>[int\w\s]+)&gt;(?P<after_second>\b\w*\b|[^\s{}]+)?)".format(punctuation), re.UNICODE)
    opening_tag = re.compile(ur'[\w{0}{1}]*\s*&lt;[int\w\s]+&gt;[\s{0}]*[\w{0}{1}]*'.format(punctuation, ACCENTS), re.UNICODE)
    closing_tag = re.compile(ur'[\w{0}{1}]*\s*&lt;\s*/[int\w\s]+&gt;[\s{0}]*[\w{0}{1}]*'.format(punctuation, ACCENTS), re.UNICODE)

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
                        if re.match(ur'[\w.{}]*'.format(ACCENTS), content, re.UNICODE).group() != content:
                            found[ln] = [4, 'Initial tag error', error_tag]

                # If text doesn't feet pattern `W. E. B.` -> error
                elif len(inner_content) > 1:
                    for content in inner_content:
                        if not re.match(ur'^\w[{}]?\.$'.format(ACCENTS), content, re.UNICODE):
                            found[ln] = [4, 'Initial tag error', error_tag]

    if not tag_exists and not found:
        found[1] = [4, 'Be sure to include initial tag for any and all initialisms. If there were no initialisms, feel free to ignore this error.', '']

    return found


#Language tag validator
def command5(filepath):

    #load the languages to array
    languages = [
        'Foreign','Acholi','Afrikaans','Albanian','Amharic','Arabic','Ashante','Assyrian','Azerbaijani','Azeri',
        'Bajuni','Basque','Batak','Behdini','Belorussian','Bengali','Berber','Betawi','Bosnian','Bravanese','Bulgarian','Burmese',
        'Cakchiquel','Cambodian','Cantonese','Catalan','Chaldean','Chamorro','Chao-chow','Chavacano','Chinese','Chuukese','Croatian',
        'Czech','Danish','Dari','Dinka','Diula','Dutch','English','Estonian','Espanol','Fante',
        'Farsi','Finnish','Flemish','French','Fukienese','Fula','Fulani','Fuzhou','Gaddang',
        'Gaelic','Gayo','Georgian','German','Gorani','Greek','Gujarati','Haitian','Creole','Hakka',
        'Hausa','Hebrew','Hindi','Hmong','Hungarian','Ibanag','Icelandic','Igbo','Ilocano',
        'Indonesian','Inuktitut','Italian','Jakartanese','Japanese','Javanese','Kanjobal','Karen','Karenni','Kashmiri',
        'Kazakh','Khmer','Kikuyu','Kinyarwanda','Kirundi','Korean','Kosovan','Kotokoli','Krio','Kurdish','Kurmanji',
        'Kyrgyz','Lakota','Laotian','Latvian','Lingala','Lithuanian','Luganda','Maay','Macedonian','Malay',
        'Malayalam','Maltese','Mandarin','Mandingo','Mandinka','Marathi','Marshallese','Mirpuri','Mixteco','Moldavan',
        'Mongolian','Montenegrin','Navajo','Neapolitan','Nepali','Nigerian','Pidgin','Norwegian','Oromo','Pahari',
        'Papago','Papiamento','Pashto','Patois','Persian','Pidgin','English','Polish','Portug.creole','Portuguese','Pothwari',
        'Pulaar','Punjabi','Putian','Quichua','Romanian','Russian','Samoan','Serbian','Shanghainese','Shona',
        'Sichuan','Sicilian','Sinhalese','Slovak','Somali','Sorani','Spanish','Sudanese','Arabic','Sundanese',
        'Susu','Swahili','Swedish','Sylhetti','Tagalog','Taiwanese','Tajik','Tamil','Telugu','Thai',
        'Tibetan','Tigre','Tigrinya','Toishanese','Tongan','Toucouleur','Trique','Tshiluba','Turkish','Ukrainian',
        'Urdu','Uyghur','Uzbek','Vietnamese','Visayan','Welsh','Wolof','Yiddish','Yoruba','Yupik',
        'Ambonese', 'Betawinese', 'Latin', 'Manadonese'
    ]

    punctuation_marks = u""":,\-'_!—".?;"""

    regex = re.compile(ur'(?P<content>(?P<before_first>\b\w*\b)?&lt;(?P<first_tag>/*\s*\w*\s*):(?P<first_tag_lang>\s*\w*\s*)&gt;(?P<inner_text>.*?)&lt;(?P<forward>[\/]*)(?P<second_tag>\s*\w*\s*):(?P<second_tag_lang>\s*\w*\s*)&gt;(?P<after_second>\b\w*\b)?)', re.UNICODE)
    opening_tag = re.compile(ur'[\w{0}{1}]*\s*&lt;\s*\w*\s*:\s*\w*\s*&gt;[\s{0}]*[\w{0}{1}]*'.format(punctuation_marks, ACCENTS), re.UNICODE)
    closing_tag = re.compile(ur'[\w{0}{1}]*\s*&lt;/\s*\w*\s*:\s*\w*\s*&gt;[\s{0}]*[\w{0}{1}]*'.format(punctuation_marks, ACCENTS), re.UNICODE)

    found = {}

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            line = line.rstrip('\r\n')

            if (
                re.search(opening_tag, line) is not None and
                re.search(closing_tag, line) is None
            ):
                open_tag = re.search(opening_tag, line).group(0)
                content = _prepare_content(open_tag)
                found[ln] = [5, "Missing closing tag", content]

            if (
                re.search(opening_tag, line) is None and
                re.search(closing_tag, line) is not None
            ):
                close_tag = re.search(closing_tag, line).group(0)
                content = _prepare_content(close_tag)
                found[ln] = [5, "Missing opening tag", content]

            matches = re.finditer(regex, line)
            for match in matches:
                if match:
                    content = match.group('content')
                    content = _prepare_content(content)

                    # Check for stucked words
                    if (
                        match.group('before_first') is not None or
                        not match.group('inner_text').startswith(" ") or
                        not match.group('inner_text').endswith(" ") or
                        match.group('after_second') is not None
                    ):
                        found[ln] = [5, "Tag syntax error", content]
                        continue

                    # Check spelling
                    if (
                        match.group('first_tag') != 'lang' or
                        match.group('second_tag') != 'lang' or
                        match.group('first_tag_lang') not in languages or
                        match.group('second_tag_lang') not in languages
                    ):
                        found[ln] = [5, "Tag syntax error", content]
                        continue

                    # Check for wrong syntax
                    if match.group('forward') != u'/':
                        found[ln] = [5, "Tag syntax error", content]
                        continue


                    inner_text = match.group('inner_text').strip()
                    if not inner_text:
                        found[ln] = [5, 'Language tag is empty', content]
                        continue

                    # Check for initial tag inside lang tag
                    if re.search(ur'(&lt;|\<)([int\w\s/\\]+)(&gt;|\>).*?(&lt;|\<)([\\/\s]*)([int\w\s]+)(&gt;|\>)', inner_text, re.UNICODE):
                        continue

                    # Check final punctuation
                    inner_text_end = inner_text[-1]
                    if inner_text_end in punctuation_marks:
                        found[ln] = [5, "Final punctuation marks should be outside the tag", content]

            ln += 1

    return found


def _prepare_content(content):
    content = content.replace('&lt;' , '<')
    content = content.replace('&gt;' , '>')
    content = content.encode('utf')
    return content


#Numeral hunter
def command6(filepath):

    found = {}

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip(" \r\n")

            #if line starts with < and ends in >
            if line.startswith('<') and line.endswith('>'):
                #we skip everythin between <>
                continue

            words = re.findall(ur'\b\w+\b', line, re.UNICODE)
            for word in words:

                if re.match(ur'\S*\d+\S*', word, re.UNICODE) and not (word.startswith('<') and word.endswith('>')):

                    index = words.index(word)
                    if index > 0:
                        content = u'{} {}'.format(words[index - 1], word).encode('utf')
                    elif index == 0 and len(words) > 1:
                        content = u'{} {}'.format(word, words[1]).encode('utf')
                    else:
                        content = u'{}'.format(word).encode('utf')

                    found[ln] = [6, 'Numerals not allowed', content]

    return found


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
        found[1] = [7, 'No fillers tags were found. Please refer to the project page to learn about the required use of filler tags.', '']

    return found


#White space validator
def command8(filepath):
    rv = {}
    patterns = ['\[[^\]*]\]', '#[^ #\.,，。\s?!~‘s-]*', '\(\(\)\)', '\(\([^\)]*\)\)']

    for pat in patterns:
        found = command8_real(f, pat)
        rv.update(found)
    return rv

def command8_real(filepath, pattern):

    reg_allowed = '[\.,，。\s?!~‘s-]'
    regex_pat = '(.)' + pattern + '(.)'

    regex = re.compile('.' + pattern + '.')

    found = {}

    with open(filepath,'r') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")

            #if line starts with < and ends in >
            if line.startswith('<') and line.endswith('>'):
                #we skip everythin between <>
                continue

            #put spaces in front/end of line, to avoid checking for startswith/endswith for each token
            line = ' ' + line + ' '

            for m in re.findall(regex, line):
                matchObj = re.match(regex_pat, m)
                if not matchObj:
                    found[ln] =  [8, 'Missing white space (syntax)', m]
                else:
                    lC = matchObj.group(1)
                    rC = matchObj.group(2)

                    #if language is not in the list
                    if not re.match('[\s　。，]', lC):
                        found[ln] =  [8, 'Missing white space (invalid left char)', lC + '/' + m]
                    elif not re.match(reg_allowed, rC):
                        found[ln] =  [8, 'Missing white space (invalid right char)', rC + '/' + m]
    return found

#UTF-8 validator
def command9(filepath):
    found = {}
    with open(filepath, 'r') as f:
        line = f.readline()
        if line.strip("\r\n") != '<?xml version="1.0" encoding="UTF-8"?>':
            found[1] = [9, 'Invalid encoding, must be UTF-8', line]
    return found

#Inaudible tag validator
def command10(filepath):

    trailing_ok = '.,，。-?! '

    found = {}

    with open(filepath) as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")

            #if line starts with < and ends in >
            if line.startswith('<') and line.endswith('>'):
                #we skip everythin between <>
                continue

            #detect repeating tags
            if re.search("\(\(\)\)\s?\(\(\)\)", line):
                found[ln] = [10, 'Cannot have more than on (()) in a row', line]
                continue

            #detect invalid tags
            if re.search("\(\(\s+\)\)", line):
                found[ln] = [10, 'Invalid tag', line]
                continue

            #detect single (a-z) tags
            if re.search("[^\(]\([a-zA-Z0-9]+\)[^\)]", line):
                found[ln] = [10, '(()) tag incorrectly written', line]
                continue

            counter = 0
            last = 'x'

            for c in list(line):

                #check for space after ))
                if last == ')' and counter == 0 and c != line[-1] and not c in trailing_ok:
                    found[ln] = [10, 'Missing training white space', line]
                    counter = 0
                    break

                if c == '(':
                    counter = counter + 1

                    #if we don't have a space before (
                    if c != line[0] and counter == 1 and not re.match('[\s\t　。，]', last):
                        found[ln] = [10, 'Missing leading white space', line]
                        counter = 0
                        break

                elif c == ')':
                    counter = counter - 1

                    #if we have a space before )
                    if (last == ' ' or last == '\t'):
                        found[ln] = [10, 'Space before closing', line]
                        counter = 0
                        break

                last = c

                if counter > 2 or counter < 0:           #more than 2 ( or )
                    found[ln] = [10, 'Space inside', line]
                    counter = 0
                    break

            #check1) if line has invalid number of open/close brackets
            if counter != 0:
                found[ln] = [10, 'Missing parenthesis', line]

    return found

#Punctuation space validator
def command11(filepath):

    regex = re.compile(ur'((\s-[^\s])|\s[\.,!?])|([\.,!?-]\s{2,})|([\.,!?][^\s])', re.UNICODE)

    found = {}

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip(" \r\n")

            #if line starts with < and ends in >
            if line.startswith('<') and line.endswith('>'):
                #we skip everythin between <>
                continue

            for m in re.findall(regex, line):
                if m:
                    found[ln] = [11, 'Punctuation spacing issue', line.encode('utf')]

    return found


#Disallowed strings
def command12(filepath):
    bad_regex = ['\sok\s', 'Dr\.', 'Dra\.', 'www\.', '[a-zA-Z]- ']
    found = {}

    with open(filepath,'r') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")

            #if line starts with < and ends in >
            if line.startswith('<') and line.endswith('>'):
                #we skip everythin between <>
                continue

            matchObj = re.search('([,!?:\.]{2,})', line)
            if matchObj:
                found[ln] = [12, 'Invalid sequence', matchObj.group(1) + ') -> '+ line]
            else:
                for bad in bad_regex:

                    if bad == 'Dr\.' or bad == 'Dra\.':
                        if re.match('.*' + bad + '.*', line):
                            found[ln] = [12, 'Disallowed string found (' + bad.replace('\\', '').strip('s') + ')', line]
                            break
                    else:
                        if re.match('.*' + bad + '.*', line , re.IGNORECASE):
                            found[ln] = [12, 'Disallowed string found (' + bad.replace('\\', '').strip('s') + ')', line]
                            break

    return found

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


#Segment length validator
def command14(filepath):

    regex = re.compile(ur'<Sync\s*time\s*=\s*"\s*([0-9\.]+)\s*"\s*/>', re.UNICODE)
    section_end_time =re.compile(ur'<Section.*?endTime="([\d.]+)', re.UNICODE)

    found = {}
    cur_time = 0

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            line = line.rstrip("\r\n")

            if re.search(section_end_time, line) is not None:
                end_time = float(re.search(section_end_time, line).group(1))

            for m in re.findall(regex, line):
                last_sync_line = ln

                seg_time = float(m)
                seg_len = seg_time - cur_time

                if seg_len > 15.0:
                    found[ln] = [14, 'Segment exceeds limit', 'Sync time="{}"; length: {} seconds'.format(seg_time, seg_len)]

                #update current time
                cur_time = seg_time

            if u'</Section>' in line:
                seg_len = end_time - cur_time

                if seg_len > 15.0:
                    found[last_sync_line] = [14, 'Segment exceeds limit', 'Sync time="{}"; length: {} seconds'.format(cur_time, seg_len)]


            ln += 1

    return found


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

    with io.open(filepath, 'r', encoding='utf') as f:
        ln = -1
        for line in f:
            ln = ln + 1

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

    return found


#Speaker labels
def command16(filepath):

    regex = re.compile('([a-z]+)="([^"]*)"')

    needed_keys = ['type', 'dialect', 'accent']

    found = {}

    with open(filepath,'r') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")

            if line == '</Speakers>':
                break

            if line.startswith('<Speaker id='):
                attrs = {'id': 'unknown', 'name':'unknown'}
                for kv in re.findall(regex, line):
                    attrs[kv[0]] = kv[1]

                missing_keys = []
                for k in needed_keys:
                    if not k in attrs:
                        missing_keys.append(k)

                if missing_keys:
                    found[ln] = [16, 'missing label', 'Speaker id=' + attrs['id'] + '|' + attrs['name']  + ' -> '+ ','.join(missing_keys)]

                elif attrs['type'] != 'male' and attrs['type'] != 'female' and attrs['type'] != 'unknown':
                    found[ln] = [16,  'type invalid', attrs['type'] ]

                elif attrs['dialect'] == '':
                    found[ln] = [16, 'dialect empty', attrs['dialect'] ]

                elif attrs['dialect'] == 'non-native' and attrs['accent'] == '':
                    found[ln] = [16, 'null accent', '']
    return found

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


#Dissalowed tag combinations
def command18(filepath):

    regex = re.compile("^\s*\[no-speech\]"+WWpunctuatio+"*" +WWwhitespace+"*\[overlap\]\s*$|^\s*\[overlap\]"+WWpunctuatio+"*" +WWwhitespace+"*\[no-speech\]\s*$|^\s*\[overlap\]"+WWpunctuatio+"*" +WWwhitespace+"*\[music\]\s*$|^\s*\[music\]"+WWpunctuatio+"*" +WWwhitespace+"*\[overlap\]\s*$|^\s*\[no-speech\]"+WWpunctuatio+"*" +WWwhitespace+"*\[music\]\s*$|^\s*\[music\]"+WWpunctuatio+"*" +WWwhitespace+"*\[no-speech\]\s*$")

    found = {}

    with open(filepath,'r') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            line = line.rstrip("\r\n")

            for m in re.findall(regex, line):
                found[ln] = [18, 'Dissallowed tag combinations!', m]

    return found


# Choppy segments
def command19(filepath):
    # Segments shorter than that amount of time in seconds
    # are potentially Chopped segments. You can control it
    # by changing this value.
    time_amount_left = 12    # Y
    # Segments that contain that number of words at the beginning
    # or at end are potentially Chopped segments. You can control
    # this by changing the value of variable.
    number_of_words = 2     # X

    partial_line_end_marks = u":,\-_!—.?;\]"
    line_end_marks = u'!.?'
    turn_end = re.compile(ur'<\s*/\s*Turn\s*>', re.UNICODE)

    found = {}
    with io.open(filepath, 'r', encoding='utf') as f:

        ln = 0
        sync_time = None
        segment_lenght = None
        in_turn = False
        check_for_choppy = False
        for line in f:
            line = line.strip(" \r\n")

            if not line:
                ln += 1
                continue

            if re.search(ur'<\s*Turn', line, re.UNICODE) is not None:
                sync_time = None
                segment_lenght = None
                chopped_at_end = False
                chopped_line_end = None
                check_for_choppy = False
                in_turn = True

            elif in_turn:

                if re.search(ur'<\s*Sync\s*time', line, re.UNICODE) is not None:
                    new_sync_time = re.search(ur'<\s*Sync\s*time\s*=\s*"\s*(?P<value>[\d.]+?)\s*"', line, re.UNICODE).group('value')
                    new_sync_time = float(new_sync_time)
                    if sync_time is not None:
                        segment_lenght = new_sync_time - sync_time

                    sync_time = new_sync_time
                    in_sync = True

                elif in_sync:

                    if line[0].islower() and segment_lenght <= time_amount_left:
                        if check_for_choppy:
                            chopped_line = _chopped_at_start(line, ln, line_end_marks, number_of_words)
                            found.update(chopped_line)
                        if chopped_at_end:
                            found[ln-2] = [19, "Choppy segment", chopped_line_end.encode('utf')]

                    if re.search(ur'[{}]$'.format(partial_line_end_marks), line, re.UNICODE) is None:
                        chopped_at_end, chopped_line_end = _check_chopped_at_end(line, number_of_words, line_end_marks)
                        check_for_choppy = True

                    else:
                        check_for_choppy = False
                        chopped_at_end = False
                        chopped_line_end = None

                    in_sync = False

            elif re.search(turn_end, line) is not None:
                in_turn = False

            ln += 1

    return found


def _check_chopped_at_end(line, number_of_words, line_end_marks):
    for index in xrange(-(number_of_words + 1), -1):
        try:
            chopped = line.split()[index]

        except IndexError:
            chopped_at_end = False
            chopped_line_end = None

        else:
            if re.search(ur'[{}]$'.format(line_end_marks), chopped, re.UNICODE) is not None:
                chopped_at_end = True
                chopped_line_end = line
                break
            else:
                chopped_at_end = False
                chopped_line_end = None

    return chopped_at_end, chopped_line_end


def _chopped_at_start(line, ln, line_end_marks, number_of_words):
    chopped_line = {}
    for index in xrange(number_of_words):
        try:
            chopped = line.split()[index]
        except IndexError:
            pass
        else:
            if (
                re.search(ur'[{}]$'.format(line_end_marks), chopped, re.UNICODE) is not None
            ):
                chopped_line[ln] = [19, "Choppy segment", line.encode('utf')]
                break

    return chopped_line


def command20(filepath):
    disallowed_punctuation = re.compile(ur"<.*?>", re.UNICODE)

    found = {}
    with io.open (filepath, 'r', encoding='utf') as f:
        ln = 0
        for line in f:
            line = line.rstrip(' \r\n')

            if line.startswith(u'<') and line.endswith(u'>'):
                ln += 1
                continue

            match = re.search(disallowed_punctuation, line)
            if match is not  None:
                found[ln] = [20, 'Disallowed punctuation', match.group().encode('utf')]

            ln += 1

    return found


#Unused speakers
def command21(filepath):
    regex = re.compile("\"spk(\d*)\"")
    speakerlist = []
    sectionspeakers = []
    found =  {}

    with open (filepath, 'r') as f:

        for line in f:
            if "speaker=" in line:
                #print line
                if re.match(".*speaker=(\"spk\d+\").*", line):
                    if re.match(".*speaker=(\"spk\d+\").*", line).group(1) not in sectionspeakers:
                        sectionspeakers.append(re.match(".*speaker=(\"spk\d+\").*", line).group(1))

    with open (filepath, 'r') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            if "<Speaker " in line:
                #print line
                nameoccurences = re.findall("name=", line)
                sp = re.match(".*(\"spk\d+\").*", line).group(1)
                if sp not in sectionspeakers:
                    found[ln] = [21, 'Unused speaker', 'Speaker id=' + sp + ' | name=' + re.match(".*name=(\".*\").*check", line).group(1) + ' not found in content.  Try Edit > Speakers > Remove unused speakers']
            elif "<Section" in line:
                break

    return found


def command22(filepath):
    found = {}
    spknames = []

    with open (filepath, 'r') as f:
        for line in f:

            if "<Speaker " in line:
                spknames.append(re.match(".*name=(\".*?\")", line).group(1))
            elif "<Section" in line:
                break

    with open (filepath, 'r') as f:
        ln = -1
        for line in f:
            ln = ln + 1
            if "<Speaker " in line:
                nameregx = re.match(".*name=(\".*?\")", line).group(1)
                if spknames.count(nameregx) > 1:
                    found[ln] = [22, 'Multiple occurences of name=' + nameregx, 'Speaker id=' + re.match(".*(\"spk\d+\").*", line).group(1) + ' | name=' + nameregx]

    return found


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


# Code errors
def command24(filepath):

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
                    found[empty_row] = [24, 'Empty row in Sync tag', '']
                sync = True
                empty_row = None
                not_empty_row = False

                if re.search(ur'\bSync\b\s*\btime\b', line, re.UNICODE) is None:
                    found[ln] = [24, 'Tag syntax error', line.encode('utf')]
                    continue

                for group in match.groups():
                    if group is not None and group != "":
                        found[ln] = [24, 'Unexpected white space in Sync tag', line.encode('utf')]
                        break

                continue

            if sync and line and re.search(closing_turn, line) is None:
                not_empty_row = True
            elif sync and not line:
                empty_row = ln

            if re.search(closing_turn, line):
                if empty_row and not_empty_row:
                    found[empty_row] = [24, 'Empty row in Sync tag', '']
                sync = False
                empty_row = None
                not_empty_row = False

            match = re.match(inspect_turn_re, line)
            if match is not None:

                if re.search(ur'\bTurn\b.*?\bstartTime\b.*?\bendTime\b.*?>', line, re.UNICODE) is None:
                    found[ln] = [24, 'Tag syntax error', line.encode('utf')]
                    continue

                for group in match.groups():
                    if group is not None and group != "":
                        found[ln] = [24, 'Unexpected white space in Turn tag', line.encode('utf')]
                        break

                continue

            if u'<Speaker' in line and line != '<Speakers>':
                if re.match(ur'<Speaker.*?/>', line, re.UNICODE) is None:
                    found[ln] = [24, 'Tag syntax error', line.encode('utf')]

    return found


# Sequential turns by same speaker
def command25(filepath):

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
                        found[ln] = [25, 'Sequential turns by the same speaker', report]

                #save speaker
                prev_spk = speaker

    return found


print "Content-type:text/html; charset=UTF-8\r\n\r\n"

cmd_ids = range(26)

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
lang = form.getvalue('lang')
json_files = []

if not form.has_key('upload_files'):
    print '<h1>No key parameter: upload_files</h1>'
    sys.exit(0)



# strip leading path from file name to avoid
# directory traversal attacks
uploaded_files = []

try:
    for fileitem in form['upload_files']:
        fn = '/tmp/' + os.path.basename(fileitem.filename)
        open( fn, 'wb').write(fileitem.file.read())
        json_files.append(fn)
except:
    fileitem = form['upload_files']
    fn = '/tmp/' + os.path.basename(fileitem.filename)
    open( fn, 'wb').write(fileitem.file.read())
    json_files.append(fn)


lst = []
x = form.getvalue('excl_cmds')

if type(x) != list and x != None:
    lst.append(x)
    for i in lst:
        cmd_ids.remove(int(i))
elif x == None:
    pass
else:
    for i in x:
        cmd_ids.remove(int(i))

#call all commands on each file found
all_stats = {'checked_files':0, 'valid_files': 0, 'total_errors':0}
file_divs = {}
transcribers = set()

for f in json_files:
    all_stats['checked_files'] = all_stats['checked_files'] + 1

    res = []
    total_errors = 0

    # Check file encoding first.
    # If encoding is not UTF-8 report this error
    # and process the next file.
    rv = command9(f)
    if rv:
        total_errors = total_errors + len(rv.keys())
        res.append(rv)

    else:

        try:
            cmd_ids.remove(9)
        except ValueError:
            pass

        for i in cmd_ids:

            # Omit command if disabled.
            if DISABLE_COMMANDS[i]:
                continue

            rv = eval("command" + str(i))(f)

            if i == 0:
                transcribers.add(rv.pop('transcriber_id', None))

            if rv:
                total_errors = total_errors + len(rv.keys())
                res.append(rv)

    file_div = ''
    if len(res) == 0:
        all_stats['valid_files'] = all_stats['valid_files'] + 1
    else:
        try:
            sync_times = build_sync_times(f)
        except UnicodeDecodeError:
            sync_times = {1: u''}

        audio_times = build_audio_times(sync_times)

        file_div = '<table border="1">' \
                 + '<tr><th>#</th><th>Line no.</th><th>Audio time</th><th>Sync time</th><th>Error Code</th><th>Error Type</th><th>Content</th></tr>';

        item_no = 0
        for found in res:
            for ln in sorted(found.keys()):
                res = found[ln]
                file_div += '<tr><td>' + str(item_no)       + '</td>' + \
                        '<td>' + str(ln).ljust(5)           + '</td>' + \
                        '<td>' + audio_times[ln] + '</td>' +\
                        '<td>' + cgi.escape(sync_times[ln]) + '</td>' + \
                        '<td>' + str(res[0])                + '</td>' + \
                        '<td>' + res[1]                     + '</td>' + \
                        '<td>' + cgi.escape(res[2])         + '</td></tr>'
                item_no = item_no + 1
        file_div += '</table>'
    file_divs[f] = [file_div, total_errors]

    all_stats['total_errors'] = all_stats['total_errors'] + total_errors


print "<html>"
print "<head>"
print "<title>Title of Report</title>"
print '<link rel="stylesheet" type="text/css" href="../style.css">'
print '<meta charset="utf-8">'
print '<meta name="viewport" content="width=device-width, initial-scale=1">'
print '<meta name="robots" content="noindex,nofollow">'
print '<meta http-equiv="Expires" content="-1">'
print "</head>"
print "<body>"

print '<div>'
print '<table border="1">'
print '<caption>Statistics</caption>'
print '<tr><td>Language</td><td>English</td></tr>'
print '<tr><td>Date</td><td>' + datetime.datetime.now().strftime("%B %d, %Y %H:%M%p %Z") + '</td></tr>'
print '<tr><td>Number of files checked</td><td>' + str(all_stats['checked_files']) + '</td></tr>'
print '<tr><td>Total number of errors found</td><td>' + str(all_stats['total_errors']) + ' (in the whole report)' + '</td></tr>'
print '<tr><td>Number of valid files</td><td>' + str(all_stats['valid_files']) + '</td></tr>'
print '<tr><td>Commands Enabled</td><td>' + ','.join(str(x) for x in cmd_ids) + '</td></tr>'
print '</table>'
print '</div>'

print '<div name="file_bookmarks">'
print '<table border="1">'
print '<caption>File Links</caption>'
print '<tr><th>#</th><th>Name</th><th>Total Errors</th></tr>'
fe = 0
for f in sorted(file_divs.keys()):
    total_errors = str(file_divs[f][1])
    print '<tr><td>' + str(fe) +'</td><td><a href="#f' + str(fe)+ '">' + f +'</a></td><td>' + total_errors + '</tr>'
    fe = fe + 1
print '</table>'
print '</div>'

print '<p>Read about how to interpret this error report by referencing our <b><a href="https://www.greencrescent.com/cWeb/validator-output-guide.html">validator output guide</a></b>.</p> '


if len(transcribers) > 1:
    print '<div><table border="1"><tr><td>Transcriber ID mismatch</td></tr></table></div>'

fe = 0
for f in sorted(file_divs.keys()):
    if file_divs[f][1] > 0:
        print '<div id="f' + str(fe) + '">'
        print '<h2>' + str(fe) + '. ' + f + '</h2>'
        print file_divs[f][0]
        print '</div>'
    fe = fe + 1
    os.remove(f)

print '</body>'
print '</html>'
