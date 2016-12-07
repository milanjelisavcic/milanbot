# !/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import logging
import codecs

import pywikibot as pb
from pywikibot import pagegenerators as pg
from pywikibot.data import api as pb_api

logging.basicConfig(level=logging.INFO)

# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# console.setFormatter(console_formatter)

logger = logging.getLogger(__name__)
# logger.addHandler(console)

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

dict_items = {
    "disambiguation": "Q4167410"
}

dict_properties = {
    "instance": "P31"
}

#    'norwegian-bokmal': 'no',
dict_languages = {
    'afrikans': 'af',
    'arabic': 'ar',
    'armenian': 'hy',
    'belorussian': 'be',
    'belorussian-taraskievica': 'be-tarask',
    'bosnian': 'bs',
    'bulgarian': 'bg',
    'catalan': 'ca',
    'cantonese': 'yue',
    'chinese': 'zh',
    'chinese-classical': 'lzh',
    'chinese-hakka': 'hak',
    'chinese-min-nan': 'nan',
    'chinese-cn': 'zh-cn',
    'chinese-hans': 'zh-hans',
    'chinese-hant': 'zh-hant',
    'chinese-hongkong': 'zh-hk',
    'chinese-mo': 'zh-mo',
    'chinese-my': 'zh-my',
    'chinese-singapore': 'zh-sg',
    'chinese-taiwanese': 'zh-tw',
    'czech': 'cs',
    'croatian': 'hr',
    'dutch': 'nl',
    'dutch-low-saxon': 'nds-nl',
    'english': 'en',
    'english-british': 'en-gb',
    'english-canadian': 'en-ca',
    'estonian': 'et',
    'esperanto': 'eo',
    'frisian-west': 'fy',
    'frisian-north': 'frr',
    'french': 'fr',
    'finish': 'fi',
    'galician': 'gl',
    'german': 'de',
    'german-austrian': 'de-at',
    'german-swiss': 'de-ch',
    'georgian': 'ka',
    'greek': 'el',
    'italian': 'it',
    'japanese': 'ja',
    'kannada': 'kn',
    'khmer': 'km',
    'korean': 'ko',
    'latvian': 'lv',
    'macedonian': 'mk',
    'malayalam': 'ml',
    'mazandarani': 'mzn',
    'norwegian-nynorsk': 'nn',
    'occitan': 'oc',
    'odia': 'or',
    'pashto': 'ps',
    'persian': 'fa',
    'polish': 'pl',
    'portuguese': 'pt',
    'portuguese-brazilian': 'pt-br',
    'ripuarian': 'ksh',
    'romanian': 'ro',
    'russian': 'ru',
    'sorani': 'ckb',
    'scots': 'sco',
    'serbian': 'sr',
    'sr-cyrillic': 'sr-ec',
    'sr-latin': 'sr-el',
    'serbocroatian': 'sh',
    'sicilian': 'scn',
    'spanish': 'es',
    'swedish': 'sv',
    'tamil': 'ta',
    'thai': 'th',
    'turkish': 'tr',
    'ukrainian': 'uk',
    'vietnamese': 'vi',
    'welsh': 'cy',
}

sparql_disambiguation = 'SELECT ?item WHERE {?item wdt:P31 wd:Q4167410 }'
sparql_disambiguation_sr = 'SELECT ?item WHERE { ?item wdt:P31 wd:Q4167410 . ' \
                           '?wiki0 <http://schema.org/about> ?item . ' \
                           '?wiki0 <http://schema.org/isPartOf> <https://sr.wikipedia.org/> }'
sparql_people = 'SELECT ?item WHERE { ?item wdt:P31 wd:Q5 . ' \
                '?wiki0 <http://schema.org/about> ?item . ' \
                '?wiki0 <http://schema.org/isPartOf> <https://sr.wikipedia.org/> }'


def transliterate(word, transliteration_table):
    converted_word = ''
    try:
        for char in word:
            if char in transliteration_table:
                transliteration_char = transliteration_table[char]
            else:
                transliteration_char = char
            converted_word += transliteration_char
    except Exception as e:
        print(e)
    return converted_word


def wd_sparql_query(repo, query):
    """
    SPARQL query retrieving generator with a Wikidata list of items
    :param repo:
    :param query: SPARQL query
    :return: generator
    """
    generator = pg.WikidataSPARQLPageGenerator(query, site=repo)
    for instance in generator:
        instance.get(get_redirect=True)
        yield instance


def wd_extract_instance_from_claim(item, wd_property):
    """
    A generator for retrieving items in a claim
    :param item: an object from which we are extracting claims
    :param wd_property: a string key for a specific claim set
    :return: generator pair of an item and a length of claim set
    """
    list_claims = item.claims.get(wd_property)
    for claim in list_claims:
        instance = claim.getTarget()
        instance.get(get_redirect=True)
        yield instance, len(list_claims)


def log_done(verbose, formatstring, *parameters):
    with codecs.open("done.log.csv", "a", encoding="utf-8") as logfile:
        formattedstring = u'%s%s' % (formatstring, '\n')

        try:
            logfile.write(formattedstring % parameters)
        except:
            exctype, value = sys.exc_info()[:2]
            print("1) Error writing to logfile on: [%s] [%s]" % (exctype, value))
            verbose = True  # now I want to see what!
        logfile.close()
    if verbose:
        print(formatstring % parameters)


def add_descriptions(repo, language, query):
    """
    Function to add description based on 'P31` property
    :param repo:
    :param language:
    :param query:
    :return:
    """
    multiple_statements_logger = logging.getLogger("multiple_statements")
    handler = logging.FileHandler('multiple_statements.log')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    multiple_statements_logger.addHandler(handler)

    no_item = 1
    for item in wd_sparql_query(repo, query):
        try:
            if not all(k in item.descriptions for k in dict_languages.values()):
                no_item += 1
                for claim_instance, length in \
                        wd_extract_instance_from_claim(item, dict_properties.get('instance')):
                    if length > 1:
                        multiple_statements_logger.info("{no}: {item}".format(no=no_item, item=item.title()))
                        break
                    labels = claim_instance.labels
                    dict_descriptions = dict()
                    for lang_code in dict_languages.values():
                        if lang_code not in item.descriptions:
                            dict_descriptions[lang_code] = labels[lang_code]
                        elif labels[lang_code] is not item.descriptions[lang_code]:
                            dict_descriptions[lang_code] = labels[lang_code]

                    if dict_descriptions:
                        summary = u'Added description for [{langs}] language.' \
                            .format(langs=','.join(sorted(map(str, dict_descriptions.keys()))))
                        logger.debug("{ith} edit {q} for the [{langs}] descriptions"
                                     .format(ith=no_item,
                                             q=item.title(),
                                             langs=','.join(sorted(map(str, dict_descriptions.keys())))))
                        item.editDescriptions(descriptions=dict_descriptions, summary=summary)

        except pb_api.APIError as e:
            multiple_statements_logger.error("{no}: API error on {item} - {message}"
                                             .format(no=no_item, item=item.title(),
                                                     message=u''.join(str(e)).encode('utf-8')))
            pass
        except ValueError as e:
            logger.error("{no}: ValueError occurred on {item} - {message}"
                         .format(no=no_item, item=item.title(), message=u''.join(str(e)).encode('utf-8')))
            pass
        except Exception as e:
            logger.error("{no}: Undefined error on {item} - {message}"
                         .format(no=no_item, item=item.title(), message=u''.join(str(e)).encode('utf-8')))
            pass


def add_labels(repo, language, title):
    """

    :param repo:
    :param language:
    :param title:
    :return:
    """
    item = pb.ItemPage(repo, title)
    item.get()
    labels = item.labels
    if language in labels:
        try:
            label = labels[language]
            translit = transliterate(label, cyrillic_transliteration)
            dict_labels = dict()
            dict_labels[dict_languages.get('sr-cyrillic')] = label
            dict_labels[dict_languages.get('sr-latin')] = translit
            summary = u'Added labels for [{}] script variations.'.format(language)

            item.editLabels(labels=dict_labels, summary=summary)
        except Exception as e:
            print(e)


def main():
    logger.info("---- start ----")
    repo = pb.Site('wikidata', 'wikidata')
    language = dict_languages.get('serbian')

    logger.info("Main referring language is: {lang}".format(lang=language))

    # title = 'Q4167410'
    # add_labels(repo, language, title)

    add_descriptions(repo, language, sparql_disambiguation_sr)

    logger.info("---- end ----")


if __name__ == '__main__':
    main()
