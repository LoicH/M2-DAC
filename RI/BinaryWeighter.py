# -*- coding: utf-8 -*-

""" 
@author: Loïc Herbelot
"""

from Weighter import Weighter

class BinaryWeighter(Weighter):
    def __init__(self, index):
        """param index: Index object"""
        super().__init__(index)
        
    def getDocWeightsForDoc(self, docId):
        stems = self.index.getTfsForDoc(docId)
        return stems 
        
    def getDocWeightsForStem(self, stem):
        docFreq = self.index.getTfsForStem(stem)
        return docFreq
        
    def getWeightsForQuery(self, query):
        return {stem:1 for stem in query.keys() }
        
