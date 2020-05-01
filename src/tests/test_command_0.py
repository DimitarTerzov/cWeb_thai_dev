# -*- coding: utf-8 -*-
from __future__ import print_function
import os

import pytest

from command_0.validator_0 import command0
from utils import temporary_file, LANGUAGE_CODES


CONTENT = [
    [u'<Trans scribe="ell-001" audio_filename="EPT_Political_news_118" version="9" version_date="200227">\n'],      # 0
    [u'<Trans scribe="bul-011" audio_filename="EPT_Political_news_118" version="9" version_date="200227">\n'],     # 1
    [u'<Trans scribe="ellis-101" audio_filename="EPT_Political_news_118" version="9" version_date="200227">\n'],    # 2
    [u'<Trans scribe="ell-a01" audio_filename="EPT_Political_news_118" version="9" version_date="200227">\n'],       # 3
    [u'<Trans scribe="ell-0010" audio_filename="EPT_Political_news_118" version="9" version_date="200227">\n'],     # 4
]


def test_command_0(tmpdir):
    for row in range(5):
        file_ = temporary_file(tmpdir, CONTENT[row])
        found = command0(file_)

        for key, value in found.items():
            print(key, value)

        if row == 2:
            assert "ellis-101" in found[0]
        if row == 3:
            assert "ell-a01" in found[0]
        if row == 4:
            assert "ell-0010" in found[0]
        if row == 0:
            assert "ell-001" in found['transcriber_id']
        if row == 1:
            assert "bul-011" in found['transcriber_id']

    #assert 0
