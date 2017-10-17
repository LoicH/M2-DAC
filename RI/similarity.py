# -*- coding: utf-8 -*-

""" 
@author: Loïc Herbelot
"""

import numpy as np
import operator

class IRmodel():
    def __init__(self, index):
        self.index = index 
        
    def getScores(self, query, normalized):
        """:param query: Dictionary of term frequencies"""
        raise NotImplementedError("Abstract method")
    
    def getRanking(self, query):
        """:param query: Dictionary of term frequencies"""
        raise NotImplementedError("Abstract method")
    
    def dictProduct(a,b):
        s = sum([a[i]*b[i] for i in a.keys() if i in b.keys()])
        return s            
        
    def dictNorm(a):
        return np.linalg.norm(list(a.values()))
    
class Vectoriel(IRmodel):
    def __init__(self, index, weighter):
        super().__init__(index)
        self.weighter = weighter
        self.norms = {}
        
    
    def getScores(self, query, normalized):
        docsID = self.index.getDocsID()
        scores = {}
        for i in docsID:
            docWeights = self.weighter.getDocWeightsForDoc(i)
            queryWeights = self.weighter.getWeightsForQuery(query)
            score = IRmodel.dictProduct(docWeights,
                                        queryWeights)
            norm = 1
            if normalized:
                if i in self.norms:
                    norm = self.norms[i]
                else:
                    norm = IRmodel.dictNorm(docWeights)
                    self.norms[i] = norm
                norm *= IRmodel.dictNorm(queryWeights)
                
            scores[i] = score/norm
        return scores

    def getRanking(self, query):
        scores = self.getScores(query, True)
        return sorted(scores.items(), key=operator.itemgetter(1))
	
