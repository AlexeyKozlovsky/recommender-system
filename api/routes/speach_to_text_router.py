from fastapi import APIRouter
from services.extractors.speech_to_text_extractor import SpeechToTextExtractor
from services.utils.youtube_parser import Parser

speech_to_text_router = APIRouter(prefix='/s2t-router')
extractor = SpeechToTextExtractor('nn_models/audio_models/vosk-model-ru-0.22')
parser = Parser(extractor)


@speech_to_text_router.get('/get-words')
async def get_words(url: str):
    result = parser.parse(url, None)
    return result
