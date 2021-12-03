import shutil

from fastapi import UploadFile

from api.consts.db import db
from api.utils.post_processing import words_to_plain_text
from services.extractors.speech_to_text_extractor import SpeechToTextExtractor
from services.utils.youtube_parser import Parser


extractor = SpeechToTextExtractor('nn_models/audio_models/project')
parser = Parser(extractor)

col = db['video']


def get_words_service(url: str):
    result = col.find_one({'url': url})
    if not result:
        words_json = parser.parse(url, None)
        if not words_json:
            return {
                'message': 'no speech'
            }

        video_to_db = {
            'url': url,
            'words': words_json,
            'plain_text': words_to_plain_text(words_json)
        }

        col.insert_one(video_to_db)
        return words_json

    if 'words' in result.keys():
        words_json = parser.parse(url, None)
        col.update_one({'url': url}, {
            '$set': {'words': words_json, 'plain_text': words_to_plain_text(words_json)}
        })
    return result


def get_words_from_file_service(input_file: UploadFile):
    temp_file_name = 'temp.mp4'
    with open(temp_file_name, 'wb') as buf:
        shutil.copyfileobj(input_file.file, buf)

    res = extractor.get_info(temp_file_name, None)
    return {
        'message': 'success',
        'words': res
    }
