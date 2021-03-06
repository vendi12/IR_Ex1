#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Mar 20, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Unittests for Index class

'''

import unittest

import settings
from index import Index
from vectorize import VSM
from scorer import BM25, TFIDF, BM25_ADPT


DOCS = ["""Niners head coach Mike Singletary will let Alex Smith remain his starting 
        quarterback, but his vote of confidence is anything but a long-term mandate.
        Smith now will work on a week-to-week basis, because Singletary has voided 
        his year-long lease on the job.
        "I think from this point on, you have to do what's best for the football team,"
        Singletary said Monday, one day after threatening to bench Smith during a 
        27-24 loss to the visiting Eagles.
        """
        ,
        """The fifth edition of West Coast Green, a conference focusing on "green" home 
        innovations and products, rolled into San Francisco's Fort Mason last week 
        intent, per usual, on making our living spaces more environmentally friendly 
        - one used-tire house at a time.
        To that end, there were presentations on topics such as water efficiency and 
        the burgeoning future of Net Zero-rated buildings that consume no energy and 
        produce no carbon emissions.
        """
        ]

QUERY = 'medications 0947'


class TestIndex(unittest.TestCase):
    doc_limit = 2
    index_path = settings.TEST_INDEX_PATH
    length_path = settings.TEST_LENGTH_PATH

    def test_create_inv_index(self):
        index = Index()
        index.create_index(list_of_strings=DOCS)
        print index.inv_index
        assert 'coach' in index.inv_index
        assert 'N_DOCS' in index.inv_index
        print "Added", index.inv_index['N_DOCS'], "docs to the index"
        assert index.inv_index['N_DOCS'] == len(DOCS)

    def test_stemmer(self):
        index = Index(stem=True)
        index.create_index(list_of_strings=DOCS)
        print index.inv_index
        assert 'environ' in index.inv_index
        assert 'N_DOCS' in index.inv_index
        print "Added", index.inv_index['N_DOCS'], "docs to the index"
        assert index.inv_index['N_DOCS'] == len(DOCS)

    def test_parse_trec8(self):
        # create new index of the TREC8 collection
        index = Index()
        # load collection and store into index
        index.create_index(path=settings.TREC8_DOCS_PATH, limit=self.doc_limit)
        index.store_dict(self.index_path, index.inv_index)
        index.store_dict(self.length_path, index.lds)
        assert 'N_DOCS' in index.inv_index
        print "Added", index.inv_index['N_DOCS'], "docs to the index"
        assert index.inv_index['N_DOCS'] == self.doc_limit
        assert 'AVG_LD' in index.lds
        print "Average document length:", index.lds['AVG_LD']

    def test_load_collection(self):
        index = Index(self.index_path, self.length_path)
        # print index.inv_index
        assert 'N_DOCS' in index.inv_index
        # print index.inv_index
        print index.inv_index['N_DOCS'], "docs in the index"
        assert index.inv_index['N_DOCS'] == len(index.lds) - 1
        assert 'AVG_LD' in index.lds
        # print index.lds
        assert 'FBIS3-51' in index.lds.keys()
        print "Average document length:", index.lds['AVG_LD']

    def test_search_tfidf(self):
        # use the pre-computed index of the TREC8 collection
        index = Index(self.index_path)
        # search index
        query = 'television state'
        # verify tfidf ranking results
        scorer = TFIDF()
        # print index.search(query, scorer)
        assert index.search(query, scorer) == [('FBIS3-51', 5.493061443340549), ('FBIS3-50', -1.0986122886681098)]

    def test_search_bm25(self):
        # use the pre-computed index of the TREC8 collection
        index = Index(self.index_path, self.length_path)
        # make sure doc length dict is loaded
        assert index.lds
        # search index
        query = 'television state'
        # verify tfidf ranking results
        scorer = BM25()
        # print index.search(query, scorer)
        assert index.search(query, scorer) == [('FBIS3-51', 1.491323635149336e-05), ('FBIS3-50', -0.000498870351770098)]

    # def test_search_bm25_adpt(self):
    #     # use the pre-computed index of the TREC8 collection
    #     index = Index(settings.INDEX_PATH, settings.LENGTH_PATH)
    #     # make sure doc length dict is loaded
    #     assert index.lds
    #     # search index
    #     query = 'television state'
    #     # verify tfidf ranking results
    #     scorer = BM25_ADPT()
    #     print index.search(query, scorer)
        # assert index.search(query, scorer) == [('FBIS3-51', 1.491323635149336e-05), ('FBIS3-50', -0.000498870351770098)]

# class TestVSM():
#     def test_vectorize(self):
#         vsm = VSM(DOCS)


if __name__ == '__main__':
    unittest.main()
