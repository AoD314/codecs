ffmpeg -i "render/image_%%05d.webp" -r 30 -c:v libvpx-vp9 -row-mt 1 -tile-columns 6 -lossless 1 -threads 16 -pass 1 -passlogfile my_passlog -y -r 30 -f nut NUL
ffmpeg -i "renderimage_%%05d.webp" -r 30 -c:v libvpx-vp9 -row-mt 1 -tile-columns 6 -lossless 1 -threads 16 -pass 2 -passlogfile my_passlog -y -r 30 video_lossless.ivf
