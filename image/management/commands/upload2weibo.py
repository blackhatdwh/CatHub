#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 weihao <weihao@weihao-PC>
#
# Distributed under terms of the MIT license.

import base64
import subprocess
import re
import sys

def upload(image_file):
    try:
        with open(image_file, 'rb') as image:
            encoded = base64.b64encode(image.read()).decode('ascii')
        with open('/dev/shm/post_data.txt', 'w') as f:
            post_data = "------WebKitFormBoundaryUv0B9upLByHosIF0\r\nContent-Disposition: form-data; name=\"b64_data\"\r\n\r\n" + encoded + "\r\n------WebKitFormBoundaryUv0B9upLByHosIF0--\r\n\r\n"
            f.write(post_data)
        
        with open('/home/blackhatdwh/CatHub/weibo_cookie.txt') as f:
            cookie = "'%s'" % f.readline()[:-1]
        
        command = "curl -s 'http://picupload.service.weibo.com/interface/pic_upload.php?ori=1&mime=image%2Fjpeg&data=base64&url=0&markpos=1&logo=&nick=0&marks=1&app=miniblog' -H 'Origin: chrome-extension://fdfdnfpdplfbbnemmmoklbfjbhecpnhf' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryUv0B9upLByHosIF0' -H 'Accept: */*' -H " + cookie + "-H 'Connection: keep-alive' -H 'DNT: 1' --data-binary @/dev/shm/post_data.txt --compressed"
        
        result = subprocess.getoutput(command)
        pid = re.search(r'(?<="pid":").*(?=")', result).group(0)
        
        still_format = ['jpg', 'png', 'bmp', 'jpeg']
        with open(image_file, 'rb') as f:
            if f.read(6) == b'GIF89a':
                is_still = False
            else:
                is_still = True
        if not is_still:
            return("http://ww1.sinaimg.cn/large/%s.gif"%pid)
        else:
            return("http://ww1.sinaimg.cn/large/%s.jpg"%pid)
    except Exception as e:
        print(str(e))
        return -1
    
if __name__ == '__main__':
    print(upload(sys.argv[1]))
