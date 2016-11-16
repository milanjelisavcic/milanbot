# !/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys

import pywikibot as pb
from pywikibot import pagegenerators as pg

cyrillic_translit = {
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
    u' ': u' '
}

dict_items = {
    "disambiguation": "Q4167410"
}

dict_properties = {
    "instance": "P31"
}

dict_langs = {
    'serbian': 'sr',
    'sr-cyrillic': 'sr-ec',
    'sr-latin': 'sr-el'
}

sparql_disambig = 'SELECT ?item WHERE {?item wdt:P31 wd:Q4167410 }'
sparql_people = 'SELECT ?item WHERE { ?item wdt:P31 wd:Q5 . ' \
                '?wiki0 <http://schema.org/about> ?item . ' \
                '?wiki0 <http://schema.org/isPartOf> <https://sr.wikipedia.org/> }'


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


def add_descriptions(repo, language, query):
    """
    Function to add description based on 'P31` property
    :param repo:
    :param language:
    :param query:
    :return:
    """
    i = 0
    for item in wd_sparql_query(repo, query):
        try:
            if not language in item.descriptions:
                for claim_instance, length in \
                        wd_extract_instance_from_claim(item, dict_properties.get('instance')):
                    if length > 1:
                        break
                    labels = claim_instance.labels
                    dict_description = dict()
                    dict_description[language] = labels[language]
                    dict_description[dict_langs.get('sr-cyrillic')] = labels[[dict_langs.get('sr-cyrillic')]]
                    dict_description[dict_langs.get('sr-latin')] = labels[dict_langs.get('sr-latinic')]

                    summary = u'Added description for [{}] language.'.format(language)
                    # elif language in labels:
                    print("Editing " + item.title() + " with the [" + language + "] description: " + language)
                    item.editDescriptions(descriptions=dict_description, summary=summary)

                    i += 1

                if i == 1:
                    sys.exit(0)

        except Exception as e:
            print("Error: ", e)
            continue


def transliterate(word, translit_table):
    converted_word = ''
    for char in word:
        transchar = ''
        if char in translit_table:
            transchar = translit_table[char]
        else:
            transchar = char
        converted_word += transchar
    return converted_word


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
            translit = transliterate(label, cyrillic_translit)
            dict_labels = dict()
            dict_labels[dict_langs.get('sr-cyrillic')] = label
            dict_labels[dict_langs.get('sr-latin')] = translit
            item.editLabels(labels=dict_labels,
                            summary=u'Added labels for language script variations.')
        except Exception as e:
            print(e)


def main():
    print("---------------")
    repo = pb.Site('wikidata', 'wikidata')
    language = dict_langs.get('serbian')
    print("Main referring language is: " + language)

    # title = 'Q4167410'
    # add_labels(repo, language, title)
    #
    # add_descriptions(repo, language, sparql_disambig)
    add_labels(repo, language, 'Q4167410')

    print("---------------")


if __name__ == '__main__':
    main()
