from typing import List

from pydantic import BaseModel

from api.models.extracted_speech import ExtractedSpeech
from api.models.extracted_text import ExtractedText


class ExtractedFeature(BaseModel):
    words: List[ExtractedSpeech]
    image_text: List[ExtractedText]
