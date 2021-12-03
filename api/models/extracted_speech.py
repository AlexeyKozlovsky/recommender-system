from pydantic import BaseModel


class ExtractedSpeech(BaseModel):
    word: str
    time_start: float
    time_end: float
    conf: float
