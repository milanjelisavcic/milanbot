import json


# Transliteration map from Cyrillic to Latin script
with open('milanbot/languages.json') as json_file:
    cyrillic_transliteration = json.load(json_file)

# Supported languages that 'MilanBot' works with
with open('milanbot/languages.json') as json_file:
    languages = json.load(json_file)

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
