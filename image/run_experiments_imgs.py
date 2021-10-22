#!/usr/bin/env python3

import subprocess


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
