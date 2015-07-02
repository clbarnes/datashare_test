import unittest
import os
import re
from urllib.request import urlopen
import urllib.error
from collections import defaultdict

dois = set()

DATA_PATH = 'data/edgelist.csv'


class EdgeListValidationTests(unittest.TestCase):
    def setUp(self):
        with open(DATA_PATH, 'r') as f:
            all_lines = f.read().splitlines()
            self.header = all_lines[0]
            self.body = all_lines[1:]
            self.header_id = {name: idx for idx, name in enumerate(self.header.split(','))}

class FileIntegrityTests(EdgeListValidationTests):
    def test_headers_match(self):
        assert self.header == 'source,target,transmitter,receptor,minimum_distance,source_doi,target_doi'

    def test_no_missing_fields(self):
        fields_re = re.compile(r'^.+,.+,.+,.+,.+,.+,.+$')
        for i, line in enumerate(self.body, 2):
            assert fields_re.match(line), 'Missing value in line {}:\n\t{}'.format(i, line)

    def test_distance_format(self):
        number_re = re.compile(r'^\d+\.\d+$')
        for i, line in enumerate(self.body, 2):
            try:
                float(line.split(',')[self.header_id['minimum_distance']])
            except ValueError:
                raise AssertionError(
                    'Field minimum_distance in line {} does not look like a number\n\t'.format(i, line))

    def get_dois(self):
        dois = defaultdict(list)
        for i, line in enumerate(self.body, 2):
            doi1, doi2 = line.split(',')[self.header_id['source_doi']:self.header_id['target_doi'] + 1]
            dois[doi1].append(i)
            dois[doi2].append(i)
        return dois

    def test_doi_format(self):
        doi_re = re.compile(r'doi:.+\..+/.+')
        dois = self.get_dois()
        for doi in dois:
            assert doi_re.match(doi), \
                "{} on line(s) {} is not a valid DOI. Does it start with 'doi:'?".format(doi, ', '.join(dois[doi]))

    def test_doi_exists(self):
        dois = self.get_dois()
        root_url = 'http://dx.doi.org/{}'
        for doi in dois:
            try:
                urlopen(root_url.format(doi))
            except urllib.error.HTTPError:
                raise AssertionError('DOI {} on line(s) {} does not exist'.format(doi, ', '.join(str(val) for val in dois[doi])))

    def test_no_whitespace(self):
        for i, line in enumerate(self.body, 2):
            assert ' ' not in line, 'Rogue whitespace in line {}'.format(i)


class DataIntegrityTests(EdgeListValidationTests):
    def test_no_duplicate_edges(self):
        edge_set = set()
        headers = self.header.split(',')
        for i, line in enumerate(self.body, 2):
            d = dict(zip(headers, line.split(',')))
            edge_str = '{source}_{target}_{transmitter}_{receptor}'.format(**d)
            assert edge_str not in edge_set, \
                'Edge {source} -> {target} ({transmitter} to {receptor}) is repeated on line {}'.format(i)

            edge_set.add(edge_str)