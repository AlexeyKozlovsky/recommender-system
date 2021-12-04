import shutil

from fastapi import UploadFile

from api.consts.db import db
from api.utils.post_processing import words_to_plain_text
from services.extractors.speech_to_text_extractor import SpeechToTextExtractor
from services.utils.youtube_parser import Parser
from services.utils.text_comarer import str_comparer


extractor = SpeechToTextExtractor('nn_models/audio_models/vosk-model-ru-0.22')
parser = Parser(extractor)

col = db['video']


def get_words_service(url: str, recognize_again: bool = False):
    result = col.find_one({'url': url})
    if recognize_again or not result:
        print('Parse')
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
        return {
            'message': 'success',
            'words': words_json,
            'plain_text': words_to_plain_text(words_json)['text']
        }

    del result['_id']
    if 'words' not in result.keys():
        words_json = parser.parse(url, None)
        plain_text = words_to_plain_text(words_json)
        col.update_one({'url': url}, {
            '$set': {'words': words_json, 'plain_text': plain_text}
        })
        result['words'] = words_json
        result['plain_text'] = plain_text
    return result


def get_plain_text_service(url: str, recognize_again: bool = False):
    res = get_words_service(url, recognize_again)
    if not res:
        return {
            'message': 'no speech',
            'text': None
        }

    return words_to_plain_text(res['words'])


def get_words_from_file_service(input_file: UploadFile):
    temp_file_name = 'temp.mp4'
    with open(temp_file_name, 'wb') as buf:
        shutil.copyfileobj(input_file.file, buf)

    res = extractor.get_info(temp_file_name, None)

    if not res:
        return {
            'message': 'no speech',
            'words': []
        }

    return {
        'message': 'success',
        'words': res
    }


def get_plain_text_from_file_service(input_file: UploadFile):
    res = get_words_from_file_service(input_file)
    if not res:
        return {
            'message': 'no speech',
            'text': None
        }

    return words_to_plain_text(res['words'])


def estimate_accuracy_service(url: str, text: str, recognize_again: bool = True):
    result = get_plain_text_service(url, recognize_again)
    if not result:
        return {
            'message': 'no speech'
        }

    return {
        'message': 'success',
        'accuracy': str_comparer(result['text'], text)
    }


def estimate_accuracy_from_file_service(input_file: UploadFile, text: str, recognize_again: bool = True):
    result = get_plain_text_from_file_service(input_file)
    if not result:
        return {
            'message': 'no speech'
        }

    return {
        'message': 'success',
        'accuracy': str_comparer(result['text'], text)
    }


async def estimate_accuracy_from_both_files_service(video_file: UploadFile, text_file: UploadFile,
                                                    recognize_again: bool = False):
    text_binary = await text_file.read()
    text = text_binary.decode()

    return estimate_accuracy_from_file_service(video_file, text, recognize_again)


async def estimate_accuracy_from_text_file_service(url: str, text_file: UploadFile,
                                                   recognize_again: bool = False):
    text_binary = await text_file.read()
    text = text_binary.decode()

    return estimate_accuracy_service(url, text, recognize_again)


def estimate_accuracy_from_dict_service(url: str, text_dict: dict):
    text = text_dict['text']
    return estimate_accuracy_service(url, text, recognize_again=True)
