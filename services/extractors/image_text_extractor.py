import cv2
import imutils
import json
import numpy as np
import os
import pandas as pd
import requests
import time
from base64 import b64encode
from pylab import rcParams
import io
import easyocr
from matplotlib import pyplot as plt

class ImageTextExtractor:
    def __init__(self, sourse_path, output_path, ap_data):
        self.sourse_p = sourse_path
        self.output_p = output_path
        # self.rcParams['figure.figsize'] = 10, 20
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

    def requestOCR(self, buff, time):
        imgdata = self.makeImageData(buff)
        response = requests.post(self.url,
                                 data=imgdata,
                                 params={'key': self.api_key},
                                 headers={'Content-Type': 'application/json'})
        response = response.json()['responses'][0]['textAnnotations']
        this_time = {'time' : time}
        response = [this_time] + response
        self.data_to_write.append(response)

    def Find_Text_On_Video(self, cur_frames=100):
        video = cv2.VideoCapture(self.sourse_p)
        video_total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        keyframe_interval = int(video_total_frames) / cur_frames
        next_keyframe = keyframe_interval / 2
        finished_frames = 0
        fps = video.get(cv2.CAP_PROP_FPS)
        all_time = video.get(cv2.CAP_PROP_FRAME_COUNT) / fps
        time_koef = all_time / cur_frames
        frame_count = 0
        
        while True:
            if finished_frames == cur_frames:
                break
            video.set(cv2.CAP_PROP_POS_FRAMES, int(next_keyframe))
            time = frame_count * time_koef
            success, image = video.read()
            retval, buffer = cv2.imencode('.jpg', image)
            jpg_as_text = b64encode(buffer).decode()
            print(jpg_as_text)
            self.requestOCR(jpg_as_text, time)
            finished_frames += 1
            frame_count += 1
            next_keyframe += keyframe_interval
        io.open(self.output_p, "w", encoding="utf-8").write(json.dumps(self.data_to_write, ensure_ascii=False))
    
    def Get_dict_of_phrases_times(self, sourse_path, output_path):
        with open(sourse_path, 'r') as read_file:
            data = json.load(read_file)
        phrases = []
        dict_of_phrases = {}
        time_now = data[0][0]['time']
        time_before = data[0][0]['time']
        for main_description in data:
            frame_phrases = main_description[1]['description'].split('\n')
            time_before = time_now
            time_now = main_description[0]['time']
            for phrase in frame_phrases:
                if phrase not in phrases:
                    dict_of_phrases[phrase] = {'time_start' : time_now, 'time_stop' : time_now}
                    phrases.append(phrase)
                else:
                    if dict_of_phrases[phrase]['time_stop'] == time_before:
                        dict_of_phrases[phrase]['time_stop'] = time_now
                    else:
                        phr = phrase + ' '
                        dict_of_phrases[phr] = {'time_start' : time_now, 'time_stop' : time_now}
                        phrases.append(phr)
        io.open(output_path, "w", encoding="utf-8").write(json.dumps(dict_of_phrases, ensure_ascii=False))
 
class ImageTextExtractor_noGoogle:
    def __init__(self, sourse_path, output_path):
        self.sourse_p = sourse_path
        self.output_p = output_path
        self.data_to_write = []
        self.IMAGE_PATH = 'dt.png'
        self.reader = easyocr.Reader(['ru', 'en'])
    
    def Find_Text_On_Video(self, cur_frames=20):
        video = cv2.VideoCapture(self.sourse_p)
        video_total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        keyframe_interval = int(video_total_frames) / cur_frames
        next_keyframe = keyframe_interval / 2
        finished_frames = 0
        fps = video.get(cv2.CAP_PROP_FPS)
        all_time = video.get(cv2.CAP_PROP_FRAME_COUNT) / fps
        time_koef = all_time / cur_frames
        frame_count = 0
        
        while True:
            if finished_frames == cur_frames:
                break
            video.set(cv2.CAP_PROP_POS_FRAMES, int(next_keyframe))
            time = frame_count * time_koef
            success, image = video.read()
            cv2.imwrite('dt.png',image);
            
            result = self.reader.readtext(self.IMAGE_PATH,paragraph="False")
            print(result)
            data_x = []
            for detection in result: 
                top_left = tuple(detection[0][0])
                bottom_right = tuple(detection[0][2])
                text = detection[1]
                data_x.append({'top_left' : top_left, 'bottom_right' : bottom_right, 'text' : text})
            
            self.data_to_write.append({'time' : 1, 'text_data' : data_x})
            
            finished_frames += 1
            frame_count += 1
            next_keyframe += keyframe_interval
        io.open(self.output_p, "w", encoding="utf-8").write(json.dumps(self.data_to_write, ensure_ascii=False))
