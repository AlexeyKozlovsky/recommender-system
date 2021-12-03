from fastapi import APIRouter

from api.services.speech_to_text import get_words_service


speech_to_text_router = APIRouter(prefix='/s2t-router')


@speech_to_text_router.get('/get-words')
async def get_words(url: str):
    return get_words_service(url)
