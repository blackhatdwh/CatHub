#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 weihao <weihao@weihao-PC>
#
# Distributed under terms of the MIT license.

# Reading an animated GIF file using Python Image Processing Library - Pillow

from PIL import Image
from PIL import GifImagePlugin
import sys
def convert(filename, need_mask):
    try:
        mask = Image.open("./mask.png")
        imageObject = Image.open(filename)
        imageObject.seek(0)
        
        output_filename = filename.split('.')[0] + '_thumbnail.jpg'
        
        width, height = imageObject.size
        if width < height:
            imageObject = imageObject.crop((0, height/2-width/2, width, height/2+width/2))
        else:
            imageObject = imageObject.crop((width/2-height/2, 0, width/2+height/2, height))
        imageObject = imageObject.resize((300, 300))
        
        imageObject = imageObject.convert('RGBA')
        mask = mask.convert('RGBA')
        
        if need_mask:
            Image.alpha_composite(imageObject, mask).convert('RGB').save(output_filename)
        else:
            imageObject.convert('RGB').save(output_filename)
        return output_filename
    except:
        return -1
if __name__ == "__main__":
    filename = sys.argv[1]
    need_mask = (filename.split('.')[-1].lower().strip() == 'gif')
    convert(filename, need_mask)
