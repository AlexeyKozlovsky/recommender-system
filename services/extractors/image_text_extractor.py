import cv2
import imutils
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import requests
import time
from base64 import b64encode
from pylab import rcParams
import io

class ImageTextExtractor:
    def __init__(self, sourse_path, output_path, ap_data):
        self.sourse_p = sourse_path
        self.output_p = output_path
        #self.rcParams['figure.figsize'] = 10, 20
        with open(ap_data, "r") as read_file:
            data = json.load(read_file)
        self.api_key = data['api-key']
        self.url = data['url']
        self.data_to_write = []
        
    def makeImageData(self, buff):
        img_req = {
            'image': {
                'content': buff
            },
            'features': [{
                'type': 'TEXT_DETECTION',
                'maxResults': 1
            }]
        }
        return json.dumps({"requests": img_req}).encode()

    def requestOCR(self, buff):
        imgdata = self.makeImageData(buff)
        response = requests.post(self.url, 
                               data = imgdata, 
                               params = {'key': self.api_key}, 
                               headers = {'Content-Type': 'application/json'})
        response = response.json()['responses'][0]['textAnnotations']
        self.data_to_write.append(response)
            
    def Find_Text_On_Video(self, cur_frames = 100):
        video = cv2.VideoCapture(self.sourse_p)
        video_total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        keyframe_interval = int(video_total_frames) / cur_frames
        next_keyframe = keyframe_interval / 2
        finished_frames = 0
        while True:
            if finished_frames == cur_frames:
                break
            video.set(cv2.CAP_PROP_POS_FRAMES, int(next_keyframe))
            success,image = video.read()
            retval, buffer = cv2.imencode('.jpg', image)
            jpg_as_text = b64encode(buffer).decode()
            print(jpg_as_text)
            self.requestOCR(jpg_as_text)
            finished_frames += 1
            next_keyframe += keyframe_interval
        io.open(self.output_p, "w", encoding="utf-8").write(json.dumps(self.data_to_write, ensure_ascii=False))
