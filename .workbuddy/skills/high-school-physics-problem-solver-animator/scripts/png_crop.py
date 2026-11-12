# -*- coding: utf-8 -*-
"""纯标准库 PNG 裁剪工具（不依赖 Pillow）：解码 → 裁剪 → 重新编码。

用法: python png_crop.py <src> <dst> <x0> <y0> <x1> <y1>
仅支持 8bit、非隔行、color type 0/2/4/6 的 PNG（本用例的试题截图即此类）。
"""
import struct
import sys
import zlib


def read_png(path):
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a png")
    pos = 8
    idat = bytearray()
    w = h = bitd = ct = interlace = None
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if typ == b"IHDR":
            w, h, bitd, ct, _comp, _filt, interlace = struct.unpack(">IIBBBBB", chunk)
        elif typ == b"IDAT":
            idat += chunk
        elif typ == b"IEND":
            break
    if bitd != 8 or interlace != 0:
        raise ValueError("unsupported png: bitdepth=%s interlace=%s" % (bitd, interlace))
    return w, h, ct, zlib.decompress(bytes(idat))


def bpp_of(ct):
    return {0: 1, 2: 3, 4: 2, 6: 4}[ct]


def unfilter(raw, w, h, bpp):
    stride = w * bpp
    out = bytearray(h * stride)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        ft = raw[p]
        p += 1
        line = bytearray(raw[p:p + stride])
        p += stride
        if ft == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 255
        elif ft == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif ft == 3:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif ft == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                if pa <= pb and pa <= pc:
                    pr = a
                elif pb <= pc:
                    pr = b
                else:
                    pr = c
                line[i] = (line[i] + pr) & 255
        elif ft != 0:
            raise ValueError("bad filter type %s" % ft)
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return out


def write_png(path, w, h, ct, pixels):
    bpp = bpp_of(ct)
    stride = w * bpp
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += pixels[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data
                + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", w, h, 8, ct, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", comp)
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    x0, y0, x1, y1 = (int(v) for v in sys.argv[3:7])
    w, h, ct, raw = read_png(src)
    bpp = bpp_of(ct)
    pix = unfilter(raw, w, h, bpp)
    x0 = max(0, x0); y0 = max(0, y0)
    x1 = min(w, x1); y1 = min(h, y1)
    cw, ch = x1 - x0, y1 - y0
    out = bytearray(ch * cw * bpp)
    for y in range(ch):
        s = ((y0 + y) * w + x0) * bpp
        d = y * cw * bpp
        out[d:d + cw * bpp] = pix[s:s + cw * bpp]
    write_png(dst, cw, ch, ct, out)
    print("src=%dx%d ct=%d -> crop=%dx%d -> %s" % (w, h, ct, cw, ch, dst))


if __name__ == "__main__":
    main()
