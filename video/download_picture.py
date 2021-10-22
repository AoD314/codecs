
# http://media.xiph.org/sintel/sintel-4k-png/00000001.png
# http://blender-mirror.kino3d.org/peach/png/big_buck_bunny_00000.png

import urllib.request
import os

def download_image(url, path):
    urllib.request.urlretrieve(url, path)

def main():
    start_frame  = 5200
    count_images = 1800
    folder_download = 'bbb-png'

    if os.path.isdir(folder_download):
        print("folder exist")
        return
    else:
        os.mkdir(folder_download)

    for i in range(count_images):
        url  = "http://media.xiph.org/BBB/BBB-1080-png/big_buck_bunny_{0:05}.png".format(i + start_frame)
        path = "bbb-png/big_buck_bunny_{0:05}.png".format(i + start_frame)
        download_image(url, path)
        print("{:7.2%}   :  ".format((i + 1) / count_images), url, " --> ", path)

    print('done.')

if __name__ == "__main__":
    main()
