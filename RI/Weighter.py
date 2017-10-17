# -*- coding: utf-8 -*-

""" 
@author: Loïc Herbelot
"""


class Weighter():
    def __init__(self, index):
        """param index: Index object"""
        self.index = index 
        
    def getDocWeightsForDoc(self, docId):
        raise NotImplementedError("Abstract method.")
        
    def getDocWeightsForStem(self, stem):
        raise NotImplementedError("Abstract method.")
        
    def getWeightsForQuery(self, query):
        raise NotImplementedError("Abstract method.")
        
