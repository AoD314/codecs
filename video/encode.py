#!/usr/bin/python3

import os

only_print = False

#codec = ['H264', 'H265']#, 'vp9', 'av1']
codec = ['vp9', 'av1']
bt    = ['1M', '4M', '16M', '64M']
fps   = ['30']
res   = [(3840, 2160)]
#res   = [(3840, 2160), (4096, 4096), (7680, 4320), (8192, 8192)]

for r in res:
    w, h = r
    for c in codec:
        for b in bt:
            for f in fps:
                cmd = 'c:/Python39/python.exe ffmpeg.py -f ' + str(f) + ' -b ' + str(b) + ' -c ' + str(c) + ' -o benchmark_' + str(w) + 'x' + str(h) + '_' + str(f) + '_'+str(b)+'_'+str(c)+'.mkv'

                if only_print:
                    print(cmd)
                else:
                    os.system(cmd)
