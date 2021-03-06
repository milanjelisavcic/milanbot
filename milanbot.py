#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot as pwb

import milanbot.util.logger as log
import milanbot.transiteration as tr
from milanbot.config import parser
from milanbot.querier import wd_sparql

logger = log.terminal_logger()
file_logger = log.file_logger("test.csv")


def main(settings):
    """
    Main function
    :return:
    """
    logger.info("Starting the bot...")

    # Get the query
    with open(settings.query, 'r') as query_file:
        sparql = query_file.read()

    # Retrieve the SPARQL results
    sparql_pages = wd_sparql(query=sparql)

    counter = 1
    for page in sparql_pages:
        instance = page.get(get_redirect=True)

        gender = page['claims'][u'P21']
        if len(gender) > 1:
            continue
        gender = gender[0].target.id
        if gender == u'Q6581097':
            gender = u'Q499327' # male
        elif gender == u'Q6581072':
            gender = u'Q1775415' # female
        elif gender == u'Q16334295':
            gender = u'Q146786' # group

        citizenships = instance['claims']['P27']
        if len(citizenships) > 1:
            continue

        citizenship = citizenships[0].target.get()
        demonyms = citizenship['claims']['P1549']

        # Determine a nationality for a person
        description = extract_demonym(demonyms, gender)

        if u'P106' not in instance['claims']:
            continue

        occupation_stack = extract_occupations(gender, instance)

        if len(occupation_stack) == 0:
            continue

        for index, x in enumerate(occupation_stack):
            if index == 0:
                description += u' {}'.format(x)
            elif index == len(occupation_stack)-1:
                description += u' и {}'.format(x)
            else:
                description += u', {}'.format(x)

        descriptions = dict()
        descriptions[u'sr'] = description
        descriptions[u'sr-ec'] = description
        descriptions[u'sr-el'] = tr.transliterate(description)
        page.editDescriptions(
            descriptions=descriptions,
            summary=u'Setting/updating Serbian descriptions: {}.'.format(description))
        print('Added description {count}: {desc}'.format(
            count=counter,
            desc=description
        ))
        counter += 1
        if counter == 1000:
            break


def extract_occupations(gender, instance):
    occupations = instance['claims'][u'P106']
    watchdog = 1
    occupation_stack = list()
    for occupation in occupations:
        occupation = occupation.target.get()
        if gender == u'Q1775415' and u'P2521' in occupation['claims']:
            occupation = occupation['claims']['P2521']
        elif gender == u'Q499327' and u'P3321' in occupation['claims']:
            occupation = occupation['claims']['P3321']
        else:
            break

        for name in occupation:
            try:
                target = name.getTarget()
                if target is not None and u'sr' == target.language:
                    occupation_stack.append(name.target.text)
                    break
            except AttributeError as e:
                print('`target`: {obj} has no object `target`: {err}'.format(
                    obj=name.getID(),
                    err=e
                ))

        watchdog += 1
        if watchdog > 5:
            break
    return occupation_stack


def extract_demonym(demonyms, gender):
    """
    Search through the list of demonyms and find the right one by gender
    :param demonyms:
    :param gender: may be male (u'Q499327') od female (u'Q1775415')
    :return: demonym in Serbian language
    """
    description = u''
    for demonym in demonyms:
        local_demonym = demonym.getTarget()
        if local_demonym.language == u'sr':
            demonym_qualifiers = demonym.qualifiers
            if 'P518' in demonym_qualifiers:
                demonym_gender = demonym_qualifiers['P518']
                if len(demonym_gender) > 1:
                    exit()
                demonym_gender = demonym_gender[0].target.id
                if demonym_gender == gender:
                    description += local_demonym.text
                    break
    return description


if __name__ == '__main__':
    settings = parser.parse_args()
    try:
        main(settings)
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Shutting down the bot...")
        pwb.stopme()
