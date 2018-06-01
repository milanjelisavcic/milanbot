from pywikibot import pagegenerators as pg


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
