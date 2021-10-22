#!/usr/bin/env python3

import subprocess
"""
    cv::Mat mat_save;
    cv::Mat mat_orig = cv::imread(orig);
    double time_enc, time_dec;
    double timer = (double)cv::getTickCount();
    for(int i = 0; i < count_repeat; ++i)
    {
        save_image(save, mat_orig, compress);
    }
    double freq = cv::getTickFrequency();
    time_enc = (((double)cv::getTickCount() - timer)/freq) / static_cast<double>(count_repeat);
    timer = (double)cv::getTickCount();
    for(int i = 0; i < count_repeat; ++i)
    {
        mat_save = cv::imread(save);
    }
    time_dec = (((double)cv::getTickCount() - timer)/freq) / static_cast<double>(count_repeat);
    double psnr = cv::PSNR(mat_orig, mat_save);
    double save_size = static_cast<double>(get_filesize(save)) / (1024.0);
    save_image(save + ".bmp", mat_orig);
    double orig_size = static_cast<double>(get_filesize(save + ".bmp")) / (1024.0);
    std::cout << "{" << std::endl;
    std::cout << std::string(cv::format("format        :%s;\n",   save.substr(save.find_last_of('.')).c_str()));
    std::cout << std::string(cv::format("params        :%d;\n",   compress));
    std::cout << std::string(cv::format("cmpr size(Kb) :%.8f;\n", save_size));
    std::cout << std::string(cv::format("orig size(Kb) :%.8f;\n", orig_size));
    std::cout << std::string(cv::format("enc  time(ms) :%.8f;\n", time_enc));
    std::cout << std::string(cv::format("dec  time(ms) :%.8f;\n", time_dec));
    std::cout << std::string(cv::format("PSNR          :%.8f;\n", psnr));
    std::cout << std::string(cv::format("width         :%d;\n", mat_orig.cols));
    std::cout << std::string(cv::format("heigth        :%d;\n", mat_orig.rows));
    std::cout << "}\n";
"""


def run_experiment(exp):
    cmd = './convert -i=' + exp
    return subprocess.getoutput(cmd)


def write_to_file(text):
    f = open('output.txt', 'a', encoding='utf-8')
    f.write(text)
    f.close()


experiments = [
    "../../imgs/1920x1080.png", "../../imgs/2880x1800.png",
    "../../imgs/3840x2160.png", "../../imgs/4096x4096.png",
    "../../imgs/7360x4912.png", "../../imgs/7680x4320.png",
    "../../imgs/8192x8192.png", "../../imgs/15360x8640.png"
]

for exp in experiments:
    print(exp)
    output = run_experiment(exp)
    write_to_file(output)
