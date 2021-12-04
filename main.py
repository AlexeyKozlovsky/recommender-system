from services.extractors.speech_to_text_extractor import SpeechToTextExtractor
from services.utils.rbc_parser import rbk_parse
from services.utils.youtube_parser import Parser

if __name__ == '__main__':
    s2t = SpeechToTextExtractor('nn_models/audio_models/vosk-model-ru-0.22')
    parser = Parser(s2t)
    parser.get_annotations('https://www.youtube.com/watch?v=7TA9LsQGd2Y')


