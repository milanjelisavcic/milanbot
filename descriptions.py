# !/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import logging
import codecs

import pywikibot as pb
from pywikibot import pagegenerators as pg
from pywikibot.data import api as pb_api

import milanbot.transiteration as tr
from milanbot import languages as langs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dict_items = {
    "disambiguation": "Q4167410"
}

dict_properties = {
    "instance": "P31"
}

sparql_disambiguation = \
    'SELECT ?item WHERE {?item wdt:P31 wd:Q4167410 }'
sparql_disambiguation_sr = \
    'SELECT ?item WHERE { ?item wdt:P31 wd:Q4167410 . ' \
    '?wiki0 schema:about ?item . ' \
    '?wiki0 schema:isPartOf <https://sr.wikipedia.org/> }'
sparql_people = \
    'SELECT ?item WHERE { ?item wdt:P31 wd:Q5 . ' \
    '?wiki0 schema:about ?item . ' \
    '?wiki0 schema:isPartOf <https://sr.wikipedia.org/> }'


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
            if not all(k in item.descriptions for k in langs.values()):
                no_item += 1
                for claim_instance, length in \
                        wd_extract_instance_from_claim(item, dict_properties.get('instance')):
                    if length > 1:
                        multiple_statements_logger.info("{no}: {item}".format(no=no_item, item=item.title()))
                        break
                    labels = claim_instance.labels
                    dict_descriptions = dict()
                    for lang_code in langs.values():
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
            translit = tr.transliterate(label)
            dict_labels = dict()
            dict_labels[langs.get('sr-cyrillic')] = label
            dict_labels[langs.get('sr-latin')] = translit
            summary = u'Added labels for [{}] script variations.'.format(language)

            item.editLabels(labels=dict_labels, summary=summary)
        except Exception as e:
            print(e)


def main():
    logger.info("---- start ----")
    repo = pb.Site('wikidata', 'wikidata')
    language = langs.get('serbian')

    logger.info("Main referring language is: {lang}".format(lang=language))

    # title = 'Q4167410'
    # add_labels(repo, language, title)

    add_descriptions(repo, language, sparql_disambiguation_sr)

    logger.info("---- end ----")


if __name__ == '__main__':
    main()
