#!/usr/bin/env python2

import subprocess
import numpy as np
import matplotlib.pyplot as plt

def run_experiments():
    f = open('output.txt', 'rt')
    text = f.read()
    f.close()    
    return text

################################## 

class Table():
    def __init__(self, frmt, enc, dec, cmpr, orig, params, psnr, w, h):
        self.format = frmt
        self.enc = float(enc)
        self.dec = float(dec)
        self.cmpr = float(cmpr)
        self.orig = float(orig)
        self.params = int(params)
        self.psnr = float(psnr)
        self.w = int(w)
        self.h = int(h)
    
    def __repr__(self):
        return repr((self.format, self.params, self.psnr, self.w, self.h, self.cmpr, self.orig, self.enc, self.dec))


###################################



def prase_all_output(out):
    list = out.split('}\n{')
    os = list[0].split('\n')

    t = []

    for i in list:
        l = i.split('\n')
        
        frmt = '' 
        enc = '' 
        dec = '' 
        cmpr = '' 
        orig = ''
        params = ''
        psnr = ''
        w = '' 
        h = ''

        for j in l:            
            if j.find('format') >= 0:
                frmt = j[j.find(":")+1:j.find(";")]
            if j.find('params') >= 0:
                params = j[j.find(":")+1:j.find(";")]
            if j.find('enc') >= 0:
                enc = j[j.find(":")+1:j.find(";")]
            if j.find('dec') >= 0:
                dec = j[j.find(":")+1:j.find(";")]
            if j.find('cmpr') >= 0:
                cmpr = j[j.find(":")+1:j.find(";")]
            if j.find('orig') >= 0:
                orig = j[j.find(":")+1:j.find(";")]
            if j.find('PSNR') >= 0:
                psnr = j[j.find(":")+1:j.find(";")]
            if j.find('width') >= 0:
                w = j[j.find(":")+1:j.find(";")]
            if j.find('heigth') >= 0:
                h = j[j.find(":")+1:j.find(";")]

        t.append(Table(frmt, enc, dec, cmpr, orig, params, psnr, w, h))

    return t

###################################

def draw_plt(y, x, yt, xt, t, leg):
    """ amount of draw < 9 """
    colors = ['#ff0000','#00ff00','#0000ff','#ffff00','#ff00ff','#00ffff','#ff8000','#000000','#c0c0c0']
    fig = plt.figure()
    plt.ylabel(yt)
    plt.xlabel(xt)
    plt.title(t)
    n = len(y) / len(x)
    width = (0.5 + (float(n) - 1.0) / ( 2.0 * float(n))) / float(n)
    ind = np.arange(len(x))
    l = []
    for i in range(n):
        yy = y[i*len(x):(i+1)*len(x)]
        l += [plt.bar(ind + i * width, yy, width, color=colors[i])[0]]

        for j in range(len(yy)):
            plt.text(ind[j] + i * width + width/2.0, yy[j] + (yy[j]/100), '%.1f' % float(yy[j]), fontsize=5, ha='center', va='bottom')

    lab = [str(i) for i in x]
    plt.xticks(ind + width * n / 2.0, lab)
    plt.legend(l, leg, loc='best')
    plt.savefig(t.replace(' ', '_').replace('(','__').replace(')','__').lower() + '.svg', dpi=314)
    #plt.show()

###################################


def grep_data_by(table, format, params, w, h):
    l = []
    for t in table:
        if format != '*' and t.format != format:
            continue
        if params != '*' and t.params != params:
            continue
        if w != '*' and t.w != int(w):
            continue
        if h != '*' and t.h != int(h):
            continue
        l += [t]
    return l

def merge_arr(a1, a2, a3 = []):
    l = []
    l += a1
    l += a2
    if a3 != []:
        l += a3
    return l

def get_array_by_table(table, val):
    a = []

    tab = sorted(table, key=lambda t:t.params)

    if val == 'params':
        for t in tab:
            a += [t.params]
    elif val == 'psnr':
        for t in tab:
            a += [t.psnr]
    elif val == 'cmpr':
        for t in tab:
            a += [t.cmpr]
    elif val == 'dec':
        for t in tab:
            a += [t.dec]
    elif val == 'enc':
        for t in tab:
            a += [t.enc]

    return a


def main():
    output = run_experiments()
    table = prase_all_output(output)

    res = [[1280, 720], [1920, 1080], [2880, 1800], [3840, 2160], [4096, 4096]]

    for r in res:
        l = grep_data_by(table, '.webp', '*', r[0], r[1])
        x = get_array_by_table(l, 'params')

        l = grep_data_by(table, '.webp', '*', r[0], r[1])
        y_webp = get_array_by_table(l, 'psnr')

        l = grep_data_by(table, '.jpeg', '*', r[0], r[1])
        y_jpeg = get_array_by_table(l, 'psnr')
        
        y = merge_arr(y_webp, y_jpeg)
        
        draw_plt(y, x, "PSNR", "Quality", 'WebP vs Jpeg (Quality-PSNR) [' + str(r[0]) + 'x' + str(r[1]) + ']', ['webp', 'jpeg'])


    for r in res:
        l = grep_data_by(table, '.webp', '*', r[0], r[1])
        x = get_array_by_table(l, 'params')

        l = grep_data_by(table, '.webp', '*', r[0], r[1])
        y_webp = get_array_by_table(l, 'cmpr')

        l = grep_data_by(table, '.jpeg', '*', r[0], r[1])
        y_jpeg = get_array_by_table(l, 'cmpr')
        
        y = merge_arr(y_webp, y_jpeg)
        
        draw_plt(y, x, "Compression Size(kb)", "Quality", 'WebP vs Jpeg (Quality-Compression Size) [' + str(r[0]) + 'x' + str(r[1]) + ']', ['webp', 'jpeg'])


    for r in res:
        l = grep_data_by(table, '.webp', '*', r[0], r[1])
        x = get_array_by_table(l, 'params')

        l = grep_data_by(table, '.webp', '*', r[0], r[1])
        y_webp = get_array_by_table(l, 'enc')

        l = grep_data_by(table, '.jpeg', '*', r[0], r[1])
        y_jpeg = get_array_by_table(l, 'enc')
        
        y = merge_arr(y_webp, y_jpeg)
        
        draw_plt(y, x, "Encoding Time(ms)", "Quality", 'WebP vs Jpeg (Quality-Encoding Time) [' + str(r[0]) + 'x' + str(r[1]) + ']', ['webp', 'jpeg'])


    for r in res:
        l = grep_data_by(table, '.webp', '*', r[0], r[1])
        x = get_array_by_table(l, 'params')

        l = grep_data_by(table, '.webp', '*', r[0], r[1])
        y_webp = get_array_by_table(l, 'dec')

        l = grep_data_by(table, '.jpeg', '*', r[0], r[1])
        y_jpeg = get_array_by_table(l, 'dec')
        
        y = merge_arr(y_webp, y_jpeg)
        
        draw_plt(y, x, "Decoding Time(ms)", "Quality", 'WebP vs Jpeg (Quality-Decoding Time) [' + str(r[0]) + 'x' + str(r[1]) + ']', ['webp', 'jpeg'])

if __name__ == "__main__":
    main()

