def words_to_plain_text(words_json):
    result = ''
    for word in words_json:
        result += f'{word["word"]} '
    return {
        'message': 'success',
        'text': result
    }


def annotations_to_plain_text(annotations):
    pass
