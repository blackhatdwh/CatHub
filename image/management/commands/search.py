#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 weihao <weihao@weihao-PC>
#
# Distributed under terms of the MIT license.

import subprocess
import json
import os.path

def search(term):
    offset = 0
    
    if os.path.isfile('/home/blackhatdwh/CatHub/cathub_offset.log'):
        with open('/home/blackhatdwh/CatHub/cathub_offset.log') as f:
            offset = int(f.read()) + 1
        with open('/home/blackhatdwh/CatHub/cathub_offset.log', 'w') as f:
            f.write(str(offset))
    else:
        with open('/home/blackhatdwh/CatHub/cathub_offset.log', 'w') as f:
            f.write(str(offset))
    
    
    
    result = json.loads(subprocess.getoutput('curl -s "http://api.giphy.com/v1/gifs/search?q=%s&api_key=sJCW72y5MenLzghYm3v6yFNqW1XRhw7C&offset=%s&limit=1"'%(term, offset)))
    # return [gif_url, credit_url]
    return [result['data'][0]['images']['original']['url'], result['data'][0]['url']]

