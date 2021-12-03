from typing import List

from pydantic import BaseModel

from api.models.extracted_feature import ExtractedFeature


class Video(BaseModel):
    video_name: str
    video_url: str
    video_tags: List[str]
    extracted_features: ExtractedFeature
