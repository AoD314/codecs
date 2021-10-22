import cv2
import numpy
from multiprocessing import Pool

count = 300
start = 5200
ifile = 'bbb-png/big_buck_bunny_{0:05}.png'
ofile = 'bbb-png-big/output_{0:05}.png'

W = 3840
H = 2160


def proc(i):
    input_file = ifile.format(i)
    print("read " + input_file)
    orig = cv2.imread(input_file)

    cols = len(orig[0])
    rows = len(orig)

    c_w = (W // cols) + 1
    c_h = (H // rows) + 1

    img = numpy.zeros((rows * c_h, cols * c_w, 3), dtype="uint8")

    for x in range(c_w):
        for y in range(c_h):
            img[rows * y:rows * (y + 1),
                cols * x:cols * (x + 1)] = orig[0:rows, 0:cols]

    cv2.imwrite(ofile.format(i), img[0:H, 0:W])


def main():
    with Pool(18) as p:
        p.map(proc, range(start, start + count))


if __name__ == '__main__':
    main()
