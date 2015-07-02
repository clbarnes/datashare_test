import unittest
import os
import re
from urllib.request import urlopen
import urllib.error

dois = set()

DATA_PATH = 'data/edgelist.csv'


class DataValidationTests(unittest.TestCase):
    def setUp(self):
        with open(DATA_PATH, 'r') as f:
            all_lines = f.read().splitlines()
            self.header = all_lines[0]
            self.body = all_lines[1:]
            self.header_id = {name: idx for idx, name in enumerate(self.header.split(','))}

    def test_headers_match(self):
        assert self.header == 'source,target,transmitter,receptor,minimum_distance,source_doi,target_doi'

    def test_no_missing_fields(self):
        fields_re = re.compile(r'^.+,.+,.+,.+,.+,.+,.+$')
        for line in self.body:
            assert fields_re.match(line)

    def test_distance_format(self):
        number_re = re.compile(r'^\d+\.\d+$')
        for line in self.body:
            dist = line.split(',')[self.header_id['minimum_distance']]
            assert number_re.match(dist)

    def get_doi_set(self):
        doi_set = set()
        for line in self.body:
            doi_set.update(line.split(',')[self.header_id['source_doi']:self.header_id['target_doi']])
        return doi_set

    def test_doi_format(self):
        doi_re = re.compile(r'doi:.+\..+/.+')
        doi_set = self.get_doi_set()
        for doi in doi_set:
            assert doi_re.match(doi)

    def test_doi_exists(self):
        doi_set = self.get_doi_set()
        root_url = 'http://dx.doi.org/{}'
        for doi in doi_set:
            try:
                urlopen(root_url.format(doi))
            except urllib.error.HTTPError:
                raise AssertionError('DOI {} does not exist'.format(doi))

    def test_no_whitespace(self):
        for line in self.body:
            assert ' ' not in line