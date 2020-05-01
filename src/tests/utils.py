import random
import string
import io


LANGUAGE_CODES = {
    u'bul': u'Bulgarian',
    u'eng': u'English',
    u'ell': u'Greek'
}


def temporary_file(tmpdir, content):
    name = _random_word()
    file_ = str(tmpdir.mkdir(name).join("{}.trs".format(name)))
    with io.open(file_, 'w', encoding='utf') as f:
        for line in content:
            f.write(line)
    return file_


def _random_word():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
