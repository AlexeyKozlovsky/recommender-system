from fastapi import FastAPI

from api.routes.speach_to_text import speech_to_text_router
from api.routes.image_to_text import image_to_text_router


app = FastAPI()


app.include_router(speech_to_text_router)
app.include_router(image_to_text_router)
