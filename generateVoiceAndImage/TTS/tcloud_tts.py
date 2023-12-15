# coding=UTF-8
import requests
import wave
import json
import base64
import time
import collections

from TTS.request_util import request, authorization

def task_process(text,filename):
    req = request()
    req.init()
    auth = authorization()
    auth.init()

    #request_data = collections.OrderedDict()
    request_data = dict()
    request_data['Action'] = 'TextToStreamAudio'
    request_data['AppId'] = auth.AppId
    request_data['Codec'] = req.Codec
    request_data['Expired'] = int(time.time()) + auth.Expired
    request_data['ModelType'] = req.ModelType
    request_data['PrimaryLanguage'] = req.PrimaryLanguage
    request_data['ProjectId'] = req.ProjectId
    request_data['SampleRate'] = req.SampleRate
    request_data['SecretId'] = auth.SecretId
    request_data['SessionId'] = req.SessionId
    request_data['Speed'] = 0.5
    #request_data['Text'] = req.Text
    request_data['Text'] = text
    request_data['Timestamp'] = int(time.time())
    request_data['VoiceType'] = 1009
    request_data['Volume'] = req.Volume

    signature = auth.generate_sign(request_data = request_data)
    header = {
        "Content-Type": "application/json",
        "Authorization": signature
    }
    url = "https://tts.cloud.tencent.com/stream"

    r = requests.post(url, headers=header, data=json.dumps(request_data), stream = True)
    '''
    if str(r.content).find("Error") != -1 :
        print(r.content)
        return
    '''
    i = 1
    wavfile = wave.open('../public/output/voice_output/'+filename+'.wav', 'wb')
    wavfile.setparams((2, 2, 8000, 0, 'NONE', 'NONE'))
    for chunk in r.iter_content(1000):
        if (i == 1) & (str(chunk).find("Error") != -1) :
            print(chunk)
            return 
        i = i + 1
        wavfile.writeframes(chunk)
        
    wavfile.close()


