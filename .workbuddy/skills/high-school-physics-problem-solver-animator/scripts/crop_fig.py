# -*- coding: utf-8 -*-
"""从试题截图中裁剪出题图区域（铁环 + 地面 + 墙面 + 磁铁），用于方式①内嵌原图。"""
import sys
from PIL import Image

SRC = r"C:\Users\19368\.workbuddy\clipboard-images\clipboard-2026-09-13T11-33-15-280Z-aac51ff9.png"
OUT = r"C:\Users\19368\Desktop\physics-animator-lab\_build\_fig_crop.png"

x0, y0, x1, y1 = [int(v) for v in sys.argv[1:5]]
im = Image.open(SRC).convert("RGB")
print("src size", im.size)
box = im.crop((x0, y0, x1, y1))
box.save(OUT)
print("crop", box.size, "->", OUT)
