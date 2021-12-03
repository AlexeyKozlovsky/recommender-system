from fastapi import FastAPI
from api.routes.speach_to_text import speech_to_text_router


app = FastAPI()
app.include_router(speech_to_text_router)
