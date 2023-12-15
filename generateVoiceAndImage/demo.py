# coding: utf-8

import json
import random
import sys
import numpy
import cv2
import os
import pyttsx3
import TTS.tcloud_tts as tts

from PIL import Image
from PIL import ImageFilter

from model.capthafactory import CaptchaFactory
from model.utils import CaptchaUtils

BACKGROUNDDIR = "./resources/bg/"

OUTPUTDIR = "../public/output/"
CHAROUTPUTDIR = OUTPUTDIR + "char_output/"
CHARBLURDIR = OUTPUTDIR + "char_blur/"
OVERLAYOUTPUTDIR = OUTPUTDIR + "overlay_output/"
VOICEOUTPUTDIR = OUTPUTDIR + "voice_output/"

HEAD = '''
    你好，请按照以下提示，依次选择图片中的字符：
'''

def char_custom_fn(single_char):
    # do something you wanted
    # return single_char.filter(ImageFilter.GaussianBlur)
    return single_char


def bg_custom_fn(bg):
    # do something you wanted
    # return bg.filter(ImageFilter.GaussianBlur)
    return bg


def main(id):
    # os.makedirs(BACKGROUNDDIR, exist_ok=True)
    os.makedirs(OUTPUTDIR, exist_ok=True)
    os.makedirs(CHAROUTPUTDIR, exist_ok=True)
    os.makedirs(CHARBLURDIR, exist_ok=True)
    os.makedirs(OVERLAYOUTPUTDIR, exist_ok=True)
    os.makedirs(VOICEOUTPUTDIR, exist_ok=True)

    project_name = "demo"
    with open("./configs/%s.json" % project_name, encoding="utf-8") as fp:
        demo_config = json.load(fp)

    demo_factory = CaptchaFactory(char_custom_fns=[char_custom_fn], bg_custom_fns=[bg_custom_fn], **demo_config)

    # index = 8
    # while index:
        # captcha = demo_factory.generate_captcha()
        # captcha.save(CHAROUTPUTDIR + "%s.png" % index)

        # word = cv2.imread(CHAROUTPUTDIR + "%s.png" % index)
        # # 高斯模糊        
        # word = cv2.GaussianBlur(word, (3, 3), 0)
        # cv2.imwrite(CHARBLURDIR + "%s.png" % index, word)
        # bg = cv2.imread(BACKGROUNDDIR + "%s.png" % index)
        # mask = 255 * numpy.ones(bg.shape, bg.dtype)

        # width, height, channel = bg.shape
        # center = (int(height/2),int(width/2))
        # # 柏松融合
        # temp = cv2.seamlessClone(word, bg, mask, center, cv2.MIXED_CLONE)
        # cv2.imwrite(OVERLAYOUTPUTDIR + "%s.png" % index, temp)

        # print(captcha.text, captcha.num)
        # index -= 1   
        
        # say = pyttsx3.init()
        # msg = HEAD + ' '.join(list(str(captcha.text))) + '。'

        # say.say(msg)
        # say.save_to_file(text=msg, filename=VOICEOUTPUTDIR + "%s.wav" % index)
        # say.runAndWait()
        
    captcha = demo_factory.generate_captcha()
    captcha.save(CHAROUTPUTDIR + "%s.png" % id)

    print('id: '+id)
    word = cv2.imread(CHAROUTPUTDIR + "%s.png" % id)
    # 高斯模糊        
    word = cv2.GaussianBlur(word, (3, 3), 0)
    cv2.imwrite(CHARBLURDIR + "%s.png" % id, word)
    bd_index = random.randint(1, 8)
    bg = cv2.imread(BACKGROUNDDIR + "%s.png" % bd_index)
    mask = 255 * numpy.ones(bg.shape, bg.dtype)

    width, height, channel = bg.shape
    center = (int(height/2),int(width/2))
    # 柏松融合
    temp = cv2.seamlessClone(word, bg, mask, center, cv2.MIXED_CLONE)
    cv2.imwrite(OVERLAYOUTPUTDIR + "%s.png" % id, temp)

    print(captcha.text, captcha.num)
    
    '''
    say = pyttsx3.init()
    msg = HEAD + ''.join(list(str(captcha.text))) + '。'
    

    say.say(msg)
    say.save_to_file(text=msg, filename=VOICEOUTPUTDIR + "%s.wav" % id)
    say.runAndWait()
    '''

    # 语音合成
    msg = HEAD + ''.join(list(str(captcha.text))) + '。'

    tts.task_process(msg,id)
    
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    id = sys.argv[1] if len(sys.argv) > 1 else 0
    main(id)
