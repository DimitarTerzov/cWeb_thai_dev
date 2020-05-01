# -*- coding: utf-8 -*-
from __future__ import print_function

import re


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


if __name__ == '__main__':
    found = command22('../files/KBS_Gag_Concert_2020_02_01.trs')
    print(len(found))

    for key in sorted(found.keys()):
        print(key, found[key])
