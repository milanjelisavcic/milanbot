# Mapping of Cyrillic to Latin alphabet
cyrillic_transliteration = {
    u'А': u'A', u'а': u'a',
    u'Б': u'B', u'б': u'b',
    u'В': u'V', u'в': u'v',
    u'Г': u'G', u'г': u'g',
    u'Д': u'D', u'д': u'd',
    u'Ђ': u'Đ', u'ђ': u'đ',
    u'Е': u'E', u'е': u'e',
    u'Ж': u'Ž', u'ж': u'ž',
    u'З': u'Z', u'з': u'z',
    u'И': u'I', u'и': u'i',
    u'Ј': u'J', u'ј': u'j',
    u'К': u'K', u'к': u'k',
    u'Л': u'L', u'л': u'l',
    u'Љ': u'Lj', u'љ': u'lj',
    u'М': u'M', u'м': u'm',
    u'Н': u'N', u'н': u'n',
    u'Њ': u'Nj', u'њ': u'nj',
    u'О': u'O', u'о': u'o',
    u'П': u'P', u'п': u'p',
    u'Р': u'R', u'р': u'r',
    u'С': u'S', u'с': u's',
    u'Т': u'T', u'т': u't',
    u'Ћ': u'Ć', u'ћ': u'ć',
    u'У': u'U', u'у': u'u',
    u'Ф': u'F', u'ф': u'f',
    u'Х': u'H', u'х': u'h',
    u'Ц': u'C', u'ц': u'c',
    u'Ч': u'Č', u'ч': u'č',
    u'Џ': u'Dž', u'џ': u'dž',
    u'Ш': u'Š', u'ш': u'š',
    u' ': u' ', u'%': u'%'
}

sparql_disambiguation = \
    'SELECT ?item WHERE {?item wdt:P31 wd:Q4167410 }'
sparql_disambiguation_sr = \
    'SELECT ?item WHERE { ?item wdt:P31 wd:Q4167410 . ' \
    '?wiki0 schema:about ?item . ' \
    '?wiki0 schema:isPartOf <https://sh.wikipedia.org/> }'
sparql_people = \
    'SELECT ?item WHERE { ?item wdt:P31 wd:Q5 . ' \
    '?wiki0 schema:about ?item . ' \
    '?wiki0 schema:isPartOf <https://sr.wikipedia.org/> }'
