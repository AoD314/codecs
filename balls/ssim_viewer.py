import re
import os
import matplotlib.pyplot as plt


def read_ssim(filename):
    p = re.compile('.*\(([.0-9]*)\)')
    lines = []
    with open(filename, 'rt') as f:
        lines = f.readlines()
    
    ssim = []
    for line in lines:
        m = p.match(line)
        if m:
            ssim.append(float(m.group(1)))

    return ssim

#    short_ssim = []
#    while len(ssim) > 0:
#        avg = sum(ssim[:100]) / 100.0
#        short_ssim.append(avg)
#        ssim = ssim[100:]
#    return short_ssim


def read_avg_ssim(filename):
    ssim = read_ssim(filename)
    return sum(ssim) / float(len(ssim))

def find_files(p):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]
    pattern = re.compile(p)
    files = []
    for f in onlyfiles:
        if pattern.match(f):
            files.append(f)
    return files

def get_sizeby_files(files):
    sizes = []
    for f in files:
        sizes.append(os.path.getsize(f) / (1024.0 * 1024.0))
    return sizes

# files = ['ssim.1M.h264.log', 'ssim.2M.h264.log', 'ssim.4M.h264.log']
# files = ['ssim.1M.h265.log', 'ssim.2M.h265.log', 'ssim.4M.h265.log']

#files = ['ssim.4M.h265.log', 'ssim.4M.h264.log']
#files = ['ssim.1M.h265.log', 'ssim.4M.h265.log', 'ssim.1M.h264.log', 'ssim.4M.h264.log']

# files = ['ssim.cpu.01M.h264.1920x1080.log','ssim.cpu.02M.h264.1920x1080.log','ssim.cpu.03M.h264.1920x1080.log','ssim.cpu.04M.h264.1920x1080.log','ssim.cpu.05M.h264.1920x1080.log']
files = find_files('ssim.cpu.(\d)+M.h264.1920x1080.log')
print('find: {}'.format(files))
sizes = get_sizeby_files(find_files('sample.cpu.(\d)+M.h264.1920x1080.mkv'))[:len(files)]
print('size: {}'.format(sizes))


# reading
Y = [read_avg_ssim(f) for f in files]
print (Y)
X = range(1, len(files)+1)
print (X)

#plt.plot(X, Y, label='SSIM')
#plt.plot(X, sizes, label='Mbytes')

plt.bar(X, sizes, label='size')
plt.bar(X, Y, label='ssim', color='red')

#plt.plot(X, Y)

#arrs = [read_ssim(f) for f in files]

# slice
#sl = [0, min ([len(a) for a in arrs])]
#Y = range(len(arrs[0]))[sl[0]:sl[1]]

#for i, f in enumerate(files): 
#    plt.plot(Y, arrs[i][sl[0]:sl[1]], label=f)

plt.title("SSIM")
plt.legend()
plt.show()
