import os
import time

import pandas as pd

import youtube_dl

from services.extractors.image_text_extractor import ImageTextExtractor


class Parser:
    """Класс для парсинга видео с youtube и выделения текста из них"""
    def __init__(self, speech_to_text_extractor,
                 headers={
                     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'
                 }):
        self.headers = headers
        self.speech_to_text_extractor = speech_to_text_extractor

    def parse(self, url, out_path):
        """Метод для парсинга видео с youtube
        url: ссылка на видео
        out_path: путь к файлу csv с результатами распознанных слов"""

        temp_video_path = 'temp.mp3'
        ydl_opts = {'outtmpl': temp_video_path, 'format': '140'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        result_json = self.speech_to_text_extractor.get_info(temp_video_path, delete=True)

        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

        return result_json

    def get_annotations(self, url):
        temp_video_path = 'temp.mp4'
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

        ydl_opts = {'outtmpl': temp_video_path, 'format': '18'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        i2t_extractor = ImageTextExtractor(temp_video_path, None, 'services/extractors/key_data.json')
        annotations = i2t_extractor.Find_Text_On_Video()
        result = []
        for annotation in annotations:
            if result != 0:
                if result[-1] == annotation['description']:
                    continue
            result.append(annotation['description'])

        return ' '.join(result)

    def from_csv(self, csv_path, out_path):
        """Метод для парсинга видео по ссылкам из csv файла
        csv_path: путь к csv файлам с ссылками на видео
        out_path: путь к файлу с csv результатами по каждому
        видео с распознанными словами"""
        urls_df = pd.read_csv(csv_path)
        urls_temp = urls_df.to_numpy()
        for i, url in enumerate(urls_temp):
            self.parse(url[0], os.path.join(out_path, f'{i}.csv'))
            print('Parsed!')
            time.sleep(1)
