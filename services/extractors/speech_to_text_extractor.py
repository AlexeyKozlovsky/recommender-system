import os
import json
import math

import vosk
import librosa
import numpy as np
import pandas as pd
import moviepy.editor as mp


class SpeechToTextExtractor:
    """Класс для того, чтобы выделить слова по аудио из видео"""
    def __init__(self, audio_model_path, conf=1):
        self.audio_model_path = audio_model_path
        self.conf = conf
        
    def _to_dict(self, df):
        result = {}
        for index, row in df.iterrows():
            if row['conf'] >= self.conf:
                result[row['word']] = []

        for index, row in df.iterrows():
            if row['conf'] >= self.conf:
                result[row['word']].append((row['start'], row['end']))
        return result
        
    def _extract_words(self, res):
        jres = json.loads(res)
        if not 'result' in jres:
            return []
        words = jres['result']
        return words
    
    def _transcribe_words(self, recognizer, bytes):
        result = []

        chunk_size = 4000
        for chunk_no in range(math.ceil(len(bytes) / chunk_size)):
            start = chunk_no * chunk_size
            end = min(len(bytes), (chunk_no + 1) * chunk_size)
            data = bytes[start : end]

            if recognizer.AcceptWaveform(data):
                words = self._extract_words(recognizer.Result())
                result += words
        result += self._extract_words(recognizer.FinalResult())

        return result
    
    def get_info(self, input_path, out_path=None, name=None):
        vosk.SetLogLevel(-1)

        # clip = mp.VideoFileClip(input_path)
        # print(clip.audio)
        # clip.audio.write_audiofile(temp_audio_path)

        sample_rate = 16000
        audio, sr = librosa.load(input_path, sr=sample_rate)

        int16 = np.int16(audio * 32768).tobytes()

        model = vosk.Model(self.audio_model_path)
        recognizer = vosk.KaldiRecognizer(model, sample_rate)

        result_json = []

        res = self._transcribe_words(recognizer, int16)
        if not res:
            return

        # for current_res in res:
        #     result_json.append({
        #         'conf': current_res[0],
        #         'time_end': current_res[1],
        #         'time_start': current_res[2],
        #         'word': current_res[3]
        #     })

        # df = pd.DataFrame.from_records(res)
        # df = df.sort_values('start')
        
        if os.path.isfile(input_path):
            os.remove(input_path)

        # df.append({'conf': name}, ignore_index=True)
        # if out_path is not None:
        #     df.to_csv(out_path, index=False)
            
        return res
