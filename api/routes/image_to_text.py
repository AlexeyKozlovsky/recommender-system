from fastapi import APIRouter

from api.services.image_to_text import get_annotations_service
from services.extractors.image_text_extractor import ImageTextExtractor

image_to_text_router = APIRouter(prefix='/i2t-extractor')
extractor = ImageTextExtractor('nn_models/audio_models/vosk-model-ru-0.22')


@image_to_text_router.get('/get_texts')
async def get_annotations(url: str):
    return get_annotations_service(url)
