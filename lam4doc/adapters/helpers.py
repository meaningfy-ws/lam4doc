#!/usr/bin/python3

# helpers.py
# Date:  18/10/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com
from rdflib.util import guess_format

INPUT_MIME_TYPES = {
    'rdf': 'application/rdf+xml',
    'trix': 'application/xml',
    'nq': 'application/n-quads',
    'nt': 'application/n-triples',
    'jsonld': 'application/ld+json',
    'n3': 'text/n3',
    'ttl': 'text/turtle',
}


def get_file_format(file: str, types: dict = None) -> str:
    """
    Helper method to check get the format of the provided file, and to check whether they are from the
    acceptable file formats.
    :param file: file location
    :param types: a dictionary of expected fle types for the file to be checked on
    :return: format of the file
    """
    if types is None:
        types = INPUT_MIME_TYPES

    file_format = guess_format(str(file), types)
    if file_format is None:
        raise ValueError(f'Format of "{file}" is not supported.')

    return file_format
