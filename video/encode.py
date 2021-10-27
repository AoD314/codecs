#!/usr/bin/python3

import os

only_print = False


def get_ffmpeg():
    return 'c:/Python39/python.exe video/ffmpeg.py'


#codec = ['H264', 'H265', 'vp9', 'av1']
codec = ['vp9']
bt = ['1M', '2M', '4M', '8M', '16M']
fps = ['30']
res = [(3840, 2160)]
# res   = [(3840, 2160), (4096, 4096), (7680, 4320), (8192, 8192), (15360 , 8640)]

for r in res:
    w, h = r
    for f in fps:
        for b in bt:
            for c in codec:
                cmd = get_ffmpeg() + f' -f {f} -b {b:3} -c {c:4} -o benchmark_{w}x{h}_{f}_{b}_{c}.mkv'

                if only_print:
                    print(cmd)
                else:
                    os.system(cmd)
