#!/usr/local/bin/python3
import logging

import pywikibot as pwb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MilanBot")

def main():
    """
    Main function
    :return:
    """
    logger.info("Starting the bot...")
    repo = pwb.Site('wikidata', 'wikidata')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Shutting down the bot...")
        pass















# import milanbot.transiteration as tr
# import milanbot
#
#
# site = pywikibot.Site('test', 'wikidata')  # any site will work, this is just
# #  an
# # example
# # page = pywikibot.Page(site, 'Douglas Adams')
# # item = pywikibot.ItemPage.fromPage(page)  # this can be used for any page object
# # you can also define an item like this
# repo = site.data_repository()  # this is a DataSite object
# item = pywikibot.ItemPage(repo, 'Q42')  # This will be functionally the same as the other item we defined
# item.get()  # you need to call it to access any data.
# sitelinks = item.sitelinks
# aliases = item.aliases
# if 'en' in item.labels:
#     print('The label in English is: ' + item.labels['en'])
# if item.claims:
#     try:
#         if 'P31' in item.claims: # instance of
#             print(item.claims['P31'][0].getTarget())
#             print(item.claims['P31'][0].sources[0])  # let's just assume it has sources.
#     except:
#         pass
#
# # Edit an existing item
# item.editLabels(labels={'sh': 'Douglas Adams'}, summary=u'Edit label')
# item.editDescriptions(descriptions={'sh': 'English writer'}, summary=u'Edit description')
# item.editAliases(aliases={'sh':['Douglas Noel Adams', 'another alias']})
# item.setSitelink(sitelink={'site': 'shwiki', 'title': 'Douglas Adams'}, summary=u'Set sitelink')
# item.removeSitelink(site='shwiki', summary=u'Remove sitelink')
#
# # You can also made this all in one time:
# data = {'labels': {'sh': 'Douglas Adams'},
#   'descriptions': {'sh': 'English writer'},
#        'aliases': {'sh': ['Douglas Noel Adams', 'another alias'], 'de': ['Douglas Noel Adams']},
#      'sitelinks': [{'site': 'shwiki', 'title': 'Douglas Adams'}]}
# item.editEntity(data, summary=u'Edit item')