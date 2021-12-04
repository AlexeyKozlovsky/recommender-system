from api.services.speech_to_text import parser
from services.extractors.image_text_extractor import ImageTextExtractor


def get_annotations_service(url: str):
    result = parser.get_annotations(url)
    if not result:
        return {
            'message': 'no annotations'
        }

    return {
        'message': 'success',
        'annotations': result
    }
