# -*- coding: utf-8 -*-
import re
import io


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

    punctuation_marks = u""":,-'_!—".?;"""

    regex = re.compile(ur'(?P<content>(?P<before_first>\b\w*\b)?&lt;(?P<first_tag>/*\s*\w*\s*):(?P<first_tag_lang>\s*\w*\s*)&gt;(?P<inner_text>.*?)&lt;(?P<forward>[\/]*)(?P<second_tag>\s*\w*\s*):(?P<second_tag_lang>\s*\w*\s*)&gt;(?P<after_second>\b\w*\b)?)', re.UNICODE)
    opening_tag = re.compile(ur'&lt;\s*\w*\s*:\s*\w*\s*&gt;', re.UNICODE)
    closing_tag = re.compile(ur'&lt;/\s*\w*\s*:\s*\w*\s*&gt;', re.UNICODE)

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


if __name__ == "__main__":
    found = command5('../files/CT_Newsevents_34.trs')
    keys = found.keys()
    sorted_keys = sorted(keys)
    print "Errors:", len(sorted_keys)
    for key in sorted_keys:
        print key, " <=> ", found[key]
