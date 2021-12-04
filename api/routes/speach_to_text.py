from fastapi import APIRouter, UploadFile, File

from api.services.speech_to_text import get_words_service, get_words_from_file_service, get_plain_text_service, \
    get_plain_text_from_file_service, estimate_accuracy_service, estimate_accuracy_from_file_service, \
    estimate_accuracy_from_both_files_service, estimate_accuracy_from_text_file_service, \
    estimate_accuracy_from_dict_service

speech_to_text_router = APIRouter(prefix='/s2t-router')


@speech_to_text_router.get('/get-words')
async def get_words(url: str, recognize_again: bool = False):
    return get_words_service(url, recognize_again)


@speech_to_text_router.get('/get-plain-text')
async def get_plain_text(url: str):
    return get_plain_text_service(url)


@speech_to_text_router.post('/get-words-from-file')
async def get_words_from_file(input_file: UploadFile = File(...)):
    return get_words_from_file_service(input_file)


@speech_to_text_router.post('/get-plain-text-from-file')
async def get_plain_text_from_file(input_file: UploadFile = File(...)):
    return get_plain_text_from_file_service(input_file)


@speech_to_text_router.post('/estimate-accuracy')
async def estimate_accuracy(url: str, text: str):
    return estimate_accuracy_service(url, text)


@speech_to_text_router.post('/estimate-accuracy-from-file')
async def estimate_accuracy_from_file(text: str, input_file: UploadFile = File(...)):
    return estimate_accuracy_from_file_service(input_file, text)


@speech_to_text_router.post('/estimate-accuracy-from-both-files')
async def estimate_accuracy_from_both_files(video_file: UploadFile = File(...), text_file: UploadFile = File(...)):
    return await estimate_accuracy_from_both_files_service(video_file, text_file)


@speech_to_text_router.post('/estimate-accuracy-from-text-file')
async def estimate_accuracy_from_text_file(url: str, text_file: UploadFile = File(...), recognize_again: bool = False):
    return await estimate_accuracy_from_text_file_service(url, text_file, recognize_again)


@speech_to_text_router.post('/estimate-accuracy-from-dict')
async def estimate_accuracy_from_dict(url: str, text_dict: dict):
    return estimate_accuracy_from_dict_service(url, text_dict)
