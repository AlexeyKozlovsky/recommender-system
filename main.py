from services.extractors.speech_to_text_extractor import SpeechToTextExtractor
from services.extractors.image_text_extractor import ImageTextExtractor
from services.utils.youtube_parser import Parser

if __name__ == '__main__':
    extractor = SpeechToTextExtractor('nn_models/audio_models/project')
    # parser = Parser(extractor)
    # parser.parse('https://www.youtube.com/watch?v=KPjxV20iI30', None)
    extractor.get_info('resources/abbr2.ogg', 'abbr_new2.json')
    # extractor = ImageTextExtractor('resources/test_video.mp4', 'test_video_out.json', 'services/extractors/key_data.json')
    # extractor.Find_Text_On_Video()

