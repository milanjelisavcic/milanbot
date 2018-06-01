# !/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
import codecs
import yagmail

import pywikibot as pb
from pywikibot.data import api as pb_api

from milanbot import sparql_disambiguation_sr as sparql
import milanbot.transiteration as tr
import milanbot.logger as log
import milanbot.querier as wdq

# Supported languages that 'MilanBot' works with
with open('milanbot/languages.json') as fobj:
    langs = json.load(fobj)

logger = log.terminal_logger()
file_logger = log.file_logger("disambiguations.csv")

dict_items = {
    "disambiguation": "Q4167410"
}

dict_properties = {
    "instance": "P31"
}


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
    logger.info("Adding descriptions...")
    no_item = 1
    for item in wdq.wd_sparql_query(repo, query):
        try:
            if not all(k in item.descriptions for k in langs.keys()):
                no_item += 1
                for claim_instance, length in \
                        wd_extract_instance_from_claim(item, dict_properties.get('instance')):
                    if length > 1:
                        file_logger.info("{item},{no}".format(
                            no=no_item,
                            item=item.title()))
                        break
                    labels = claim_instance.labels
                    dict_descriptions = dict()
                    for lang_code in langs.keys():
                        if lang_code not in item.descriptions and lang_code in labels:
                            dict_descriptions[lang_code] = labels[lang_code]

                    if dict_descriptions:
                        summary = u'Add description in [{langs}] language(s).' \
                            .format(langs=','.join(sorted(map(str, dict_descriptions.keys()))))
                        file_logger.info("{q},{ith},[{langs}]".format(
                            ith=no_item,
                            q=item.title(),
                            langs=','.join(sorted(map(str, dict_descriptions.keys())))))
                        item.editDescriptions(descriptions=dict_descriptions, summary=summary)

        except pb_api.APIError as e:
            file_logger.error("{item},{no},{message}".format(
                no=no_item,
                item=item.title(),
                message=u''.join(str(e)).encode('utf-8')))
            pass
        except ValueError as e:
            file_logger.error("{item},{no},{message}".format(
                no=no_item,
                item=item.title(),
                message=u''.join(str(e)).encode('utf-8')))
            pass
        except Exception as e:
            file_logger.error("{item},{no},{message}".format(
                no=no_item,
                item=item.title(),
                message=u''.join(str(e)).encode('utf-8')))
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
            dict_labels['sr-ec'] = label
            dict_labels['sr-el'] = translit
            summary = u'Added labels for [{}] script variations.'.format(language)

            item.editLabels(labels=dict_labels, summary=summary)
        except Exception as e:
            print(e)


def main():
    repo = pb.Site('wikidata', 'wikidata')
    language = 'sr'
    add_descriptions(repo, language, sparql)

if __name__ == '__main__':
    try:
        logger.info("Starting the bot...")
        main()
    except KeyboardInterrupt:
        pass
    finally:
        pass