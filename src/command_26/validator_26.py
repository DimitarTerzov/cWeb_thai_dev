# -*- coding: utf-8 -*-
from __future__ import print_function
import io

# Omissions
def command26(filepath):

    found = {}
    with io.open(filepath, 'r', encoding='utf') as f:

        in_section = False
        periods = 0
        commas = 0
        exclamations = 0
        questions = 0
        for line in f:
            line = line.rstrip("\r\n")

            if '<Section' in line:
                in_section = True

            if in_section and not line.startswith('<'):
                periods += line.count('.')
                commas += line.count(',')
                exclamations += line.count('!')
                questions += line.count('?')

        if (periods < 20 or commas == 0 or
            exclamations == 0 or questions == 0):
            found['warning_message'] = 'Please check your file for proper punctuation. \
You should use periods, question marks, exclamation points, \
commas and hyphens for hyphenated words as normal.'

    return found
