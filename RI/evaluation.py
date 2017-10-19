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
    def __init__(self, irlist):
        self.irlist = irlist

    def getRelevantResults(self):
        # The relevant results of the query are the ones that have
        # a score higher than minimum:
        minScore = min([score for (docId, score) in self.irlist.getScores()])
        relevantResults = [docId for (docId, score) in self.irlist.getScores()
                          if score > minScore]
        return relevantResults

    def precisionAt(self, i):
        """ Return the number of real relevant results found, divided by i
        """
        # The true relevants results are the one in Query.relevants
        trueRels = list(self.irlist.getQuery().getRelevants().keys())
        # Relevant results we found in the query:
        relevantFound = np.intersect1d(self.getRelevantResults(),
                                    trueRels)
        return len(relevantFound)/i

    def recallAt(self, i):
        firstRelevantResults = self.getRelevantResults()[:i]
        # The true relevants results are the one in Query.relevants
        # but don't take more than i results
        trueRels = list(self.irlist.getQuery().getRelevants().keys())[:i]
        relevantFound = np.intersect1d(firstRelevantResults, trueRels)
        print("True relevant found among the first %d results: %d, should be %d"
                % (i, len(relevantFound), len(trueRels)))
        return len(relevantFound) / len(trueRels)



    def eval(self):
        return [(self.precisionAt(i), self.recallAt(i))
                for i in range(1, len(self.irlist.getScores()), 10)]
