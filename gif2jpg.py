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
mask = Image.open("./mask.png")
imageObject = Image.open("./d.gif")
imageObject.seek(0)

segments = imageObject.filename.split('.')[:-1]
filename = ''
for seg in segments:
    filename = filename + seg + '.' 
filename += 'jpg'

width, height = imageObject.size
if width < height:
    imageObject = imageObject.crop((0, height/2-width/2, width, height/2+width/2))
else:
    imageObject = imageObject.crop((width/2-height/2, 0, width/2+height/2, height))
imageObject = imageObject.resize((300, 300))

imageObject = imageObject.convert('RGBA')
mask = mask.convert('RGBA')


Image.alpha_composite(imageObject, mask).convert('RGB').save(filename)
