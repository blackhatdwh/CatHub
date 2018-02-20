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
imageObject = Image.open("./cat.gif")
imageObject.seek(0)

segments = imageObject.filename.split('.')[:-1]
filename = ''
for seg in segments:
    filename = filename + seg + '.' 
filename += 'bmp'

width, height = imageObject.size
if width < 300 or height < 300:
    imageObject = imageObject.resize((300, 300))
imageObject = imageObject.crop((width/2-150, height/2-150, width/2+150, height/2+150))

imageObject = imageObject.convert('RGBA')
mask = mask.convert('RGBA')


Image.alpha_composite(imageObject, mask).save(filename)

