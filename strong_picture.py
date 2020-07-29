#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: pfq time: 2020/7/28 0028

from PIL import Image
from PIL import ImageEnhance

for i in range(5) :
    image = Image.open('res\\pic' + str(i) + '.jpg')
    # 亮度增强
    enh_bri = ImageEnhance.Brightness(image)
    brightness = 0.7
    image_brightened = enh_bri.enhance(brightness)
    image_brightened.save('res\\pic' + str(i) + '_bri.jpg')

    # 色度增强
    enh_col = ImageEnhance.Color(image)
    color = 1.5
    image_colored = enh_col.enhance(color)
    image_colored.save('res\\pic' + str(i) + '_col.jpg')

    # 对比度增强
    enh_con = ImageEnhance.Contrast(image)
    contrast = 1.5
    image_contrasted = enh_con.enhance(contrast)
    image_contrasted.save('res\\pic' + str(i) + '_con.jpg')

    # 锐度增强
    enh_sha = ImageEnhance.Sharpness(image)
    sharpness = 3.0
    image_sharped = enh_sha.enhance(sharpness)
    image_sharped.save('res\\pic' + str(i) + '_sha.jpg')
