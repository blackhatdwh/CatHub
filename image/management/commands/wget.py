#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 weihao <weihao@weihao-PC>
#
# Distributed under terms of the MIT license.

import subprocess, sys
def download(url, filename):
    try:
        output = subprocess.check_output('wget %s -q -O %s --user-agent="Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"' % (url, filename), shell=True, timeout=30)
    except subprocess.CalledProcessError as e:
        return e.returncode
    return 0

if __name__ == '__main__':
    download(sys.argv[1], sys.argv[2])
