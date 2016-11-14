# !/usr/local/bin/python
# -*- coding: utf-8 -*-


import pywikibot as pb
from pywikibot import pagegenerators as pg

items_dict = {
    "disambiguation": "Q4167410"
}

properties_dict = {
    "instance": "Q31"
}

sparql_disambig = 'select ?item where {?item wdt:P31 wd:Q4167410 }'


def wd_sparql_query(qurey):
    site_wikidata = pb.Site('wikidata', 'wikidata')
    generator = pg.WikidataSPARQLPageGenerator(qurey, site=site_wikidata)
    for wd in generator:
        wd.get(get_redirect=True)
        yield wd


def main():
    print("---------------")
    for item in wd_sparql_query(sparql_disambig):
        try:
            if 'sr' in item.labels and 'sr' in item.descriptions:
                print(item.labels['sr'] + ": " +
                      item.descriptions['sr'])
            elif 'sr' in item.labels:
                print(item.labels['sr'])
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    main()
