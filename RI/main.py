#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ParserCACM
import TextRepresenter
import Index
import BinaryWeighter
import similarity

# TODO:
# - change Index.docs to add 'pos' and 'len' support
# - change inverted index construction to add term frequency.

if __name__ == "__main__":
    cacm_txt = "cacm/cacm.txt"

    # Construct the index:
    idx = Index.Index("cacm", "gendata/")
    stemmer = TextRepresenter.PorterStemmer()
    idx.indexation(cacm_txt, ParserCACM.ParserCACM(),
                   stemmer)
                   
    print("###### A bit of testing: ###### ")
    print("Retrieve stems in doc 20:")
    print(idx.getTfsForDoc(20))
    print("""Should look like 
    “Accelerating Convergence of Iterative Processes
A technique is discussed which, when applied
to an iterative procedure for the solution of
an equation, accelerates the rate of convergence if
the iteration converges and induces convergence if
the iteration diverges.  An illustrative example is given.”""")

    print("Retrieve docs that contains 'iter':")
    print(idx.getTfsForStem("iter"))
    print("Should include doc 20")
    
    print("###### Testing BinaryWeighter: ###### ")
    bw = BinaryWeighter.BinaryWeighter(idx)
    print("bw.getDocWeightsForDoc(20):", bw.getDocWeightsForDoc(20))
    print("bw.getDocWeightsForStem(\"iter\"):", bw.getDocWeightsForStem("iter"))
    query = stemmer.getTextRepresentation("Convergence of Iterative Processes")
    print("bw.getWeightsForQuery(query):", bw.getWeightsForQuery(query))
    

    print("###### Testing Vectoriel: ###### ")
    vect = similarity.Vectoriel(idx, bw)
    print(vect.getRanking(query))
    
                   
    
