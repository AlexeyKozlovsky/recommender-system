from fastapi import APIRouter, UploadFile, File

from api.services.speech_to_text import get_words_service, get_words_from_file_service

speech_to_text_router = APIRouter(prefix='/s2t-router')


@speech_to_text_router.get('/get-words')
async def get_words(url: str):
    return get_words_service(url)


@speech_to_text_router.post('/get-words-from-file')
async def get_words_from_file(input_file: UploadFile = File(...)):
    return get_words_from_file_service(input_file)
