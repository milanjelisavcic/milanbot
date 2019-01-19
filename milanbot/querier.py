import pywikibot as pwb
from pywikibot import pagegenerators as pg


def wd_sparql(query, repo=pwb.Site('wikidata', 'wikidata')):
    """
    Generator retrieving a Wikidata list of items from a SPARQL query
    :param query: SPARQL query
    :param repo: Wikibase repository on which to query
    :return: One item in a form of `ItemPage` per iteration
    """
    generator = pg.WikidataSPARQLPageGenerator(query, site=repo)
    for instance in generator:
        if instance.exists():
            instance.get(get_redirect=True)
            yield instance


def wd_file(file, repo=pwb.Site('wikidata', 'wikidata')):
    """
    Generator retrieving a Wikidata list of items from a CSV file
    :param file: CSV file containing a list of Q-numbers
    :param repo: Wikibase repository on which to query
    :return: One item in a form of `ItemPage` per iteration
    """
    repo=repo.data_repository()
    csv_file=open(file, 'r')
    for line in csv_file:
        qid=line[line.find('Q'):line.find(',')]
        if len(qid)>0:
            item=pwb.ItemPage(repo,qid)
            item.get(get_redirect=True)
            yield item


def wd_range(begin, end, repo=pwb.Site('wikidata', 'wikidata')):
    """
    Generator retrieving a Wikidata list of items from a rage of IDs
    :param begin: Beginning number of Q-number range
    :param end: Ending number of Q-number range
    :param repo: Wikibase repository on which to query
    :return: One item in a form of `ItemPage` per iteration
    """
    repo = repo.data_repository()
    for qid in range(begin, end, -1):
        try:
            wd = pwb.ItemPage(repo, 'Q{}'.format(qid))
            if not wd.isRedirectPage():
                if wd.exists():
                    wd.get(get_redirect=True)
                    yield wd
            else:
                pass
            qid -= 1
        except:
            pass
