from fastapi import APIRouter

from services.extractors.image_text_extractor import ImageTextExtractor

image_to_text_router = APIRouter(prefix='/i2t-extractor')
extractor = ImageTextExtractor('nn_models/audio_models/vosk-model-ru-0.22')


@image_to_text_router.get('/get_texts')
async def get_texts(url: str):
    pass

