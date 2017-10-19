#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import query
import numpy as np

class IRList():
    """ Contains a query and the scores found for this query """
    def __init__(self, query, scores):
        self.query = query
        self.scores = scores # List [(docId, score)]

    def getQuery(self):
        return self.query

    def getScores(self):
        return self.scores


class EvalMeasure:
    """ The abstract class for measure methods """
    def eval(irlist):
        """:param irlist: The IRList object that contains the query and
                          the docs found for that query"""

        raise NotImplementedError("Abstract method")


class PrecisionRecallMeasure(EvalMeasure):

    def getRelevantResults(irlist):
        # The relevant results of the query are the ones that have
        # a score higher than minimum:
        minScore = min([score for (docId, score) in irlist.getScores()])
        relevantResults = [docId for (docId, score) in irlist.getScores()
                          if score > minScore]

    def precisionAt(i, irlist):
        """ Return the number of real relevant results found, divided by i
        """
        # The true relevants results are the one in Query.relevants
        trueRels = list(irlist.getQuery().getRelevants().keys())
        # Relevant results we found in the query:
        relevantFound = np.intersect1d(getRelevantResults(irlist),
                                    trueRels)
        return len(relevantFound)/i

    def recallAt(i, irlist):
        firstRelevantResults = getRelevantResults(irlist)[:i]
        # The true relevants results are the one in Query.relevants
        trueRels = list(irlist.getQuery().getRelevants().keys())
        relevantFound = np.intersect1d(firstRelevantResults, trueRels)
        return len(relevantFound) / len(trueRels)



    def eval(irlist):
        return [(precisionAt(i, irlist), recallAt(i, irlist))
                for i in range(1, len(irlist.getScores()))]
