from services.extractors.speech_to_text_extractor import SpeechToTextExtractor
from services.utils.youtube_parser import Parser

if __name__ == '__main__':
    extractor = SpeechToTextExtractor('nn_models/audio_models/vosk-model-small-ru-0.4')
    parser = Parser(extractor)
    parser.from_csv('resources/urls.csv', 'resources/')

