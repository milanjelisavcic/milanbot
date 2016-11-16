# !/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys

import pywikibot as pb
from pywikibot import pagegenerators as pg

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


def main():
    print("---------------")
    repo = pb.Site('wikidata', 'wikidata')
    language = dict_langs.get('serbian')
    print("Main referring language is: " + language)

    i = 0
    for item in wd_sparql_query(repo, sparql_disambig):
        try:
            if not language in item.descriptions:
                # print(item.labels[language] + ": " +
                #       item.descriptions[language])
                for claim_instance, length in wd_extract_instance_from_claim(item,
                                                                             dict_properties.get('instance')):
                    # x = claim_instance.labels
                    labels = claim_instance.labels
                    if length > 1:
                        pass
                    elif language in labels:
                        label = labels[language]
                        print("Editing " + item.title() + " with description " + label)
                        item.editDescriptions(descriptions={language: label},
                                              summary=u'Added description for [{}] language.'.format(language))
                        i += 1

                    if i == 1:
                        sys.exit(0)

        except Exception as e:
            print("Error: ", e)
            pass
    print("---------------")


if __name__ == '__main__':
    main()
