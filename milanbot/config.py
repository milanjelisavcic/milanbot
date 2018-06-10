import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "-l", "--language",
    default='sr',
    type=str,
    help="Default used language for over which editing is focused."
)

parser.add_argument(
    "-q", "--query",
    default="queries/disambiguations.rq",
    type=str,
    help="A path to used SPARQL query."
)