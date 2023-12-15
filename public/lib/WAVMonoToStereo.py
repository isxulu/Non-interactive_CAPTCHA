# 用于将合成的单通道wav文件转成双通道
import wave
import struct
import os
import argparse


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--source_root', type=str, default='./single_wavs')
    parse.add_argument('--target_root', type=str, default='./wavs')
    args = parse.parse_args()

    source_root = args.source_root
    target_root = args.target_root
    data_file = sorted(os.listdir(source_root))
    if not os.path.exists(args.target_root): os.makedirs(args.target_root, exist_ok=True)

    # 打开单通道的 WAV 文件
    for file in data_file:
        if file == '.DS_Store': continue
        with wave.open(os.path.join(source_root, file), 'rb') as infile:
            # 获取 WAV 文件的参数
            params = infile.getparams()
            framerate = params.framerate
            nchannels = params.nchannels
            sampwidth = params.sampwidth
            nframes = params.nframes
            comptype = params.comptype
            compname = params.compname

            # 打开双通道的 WAV 文件
            with wave.open(os.path.join(target_root, file), 'wb') as outfile:
                # 设置 WAV 文件的参数
                outfile.setparams((2, sampwidth, framerate, nframes, comptype, compname))
                # 读取单通道 WAV 文件的每个采样点
                for i in range(nframes):
                    # 从单通道 WAV 文件中读取一个采样点
                    data = infile.readframes(1)
                    # 将该采样点的数据转换为双通道格式并写入新的 WAV 文件
                    outfile.writeframes(data + data)

    print("Done!")