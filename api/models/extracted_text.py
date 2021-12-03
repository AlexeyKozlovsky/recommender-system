from pydantic import BaseModel


class ExtractedText(BaseModel):
    text: str
    position: (float, float)
    size: (float, float)
    time_start: float
    time_end: float
