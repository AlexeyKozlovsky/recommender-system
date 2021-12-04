from services.extractors.emotions_extractor import ImageTextExtractor
from services.extractors.speech_to_text_extractor import SpeechToTextExtractor
from services.utils.youtube_parser import Parser

s2t_extractor = SpeechToTextExtractor('nn_models/audio_models/vosk-model-ru-0.22')
parser = Parser(s2t_extractor)
