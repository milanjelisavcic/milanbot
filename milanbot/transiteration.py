from . import cyrillic_transliteration as rosetta_stone


def transliterate(text, rosetta=rosetta_stone):
    """
    Transliterates given text from Cyrillic to Latin script.
    If a character is not presented in the transliteration map, it is copied
    as it is, because it should probably remain in the original form.
    :param text: A Cyrillic text to transliterate
    :param rosetta: A mapping table of possible characters
    :return: A transliterated text
    """
    transliteration = u''
    try:
        for char in text:
            if char in rosetta:
                transliteration_char = rosetta[char]
            else:
                transliteration_char = char
            transliteration += transliteration_char
    except Exception as e:
        print(e)
    return transliteration
