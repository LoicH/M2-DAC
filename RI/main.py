#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ParserCACM
import TextRepresenter
import indexation
import modeles


if __name__ == "__main__":
    cacm_txt = "cacm/cacm.txt"

    # Construct the index:
    idx = indexation.Index("cacm", "gendata/")
    stemmer = TextRepresenter.PorterStemmer()
    idx.indexation(cacm_txt, ParserCACM.ParserCACM(),
                   stemmer)
                   
    print("\n###### A bit of testing: ###### ")
    print("Retrieve stems in doc 20:")
    print(idx.getTfsForDoc(20))
    print("""Should look like 
    “Accelerating Convergence of Iterative Processes
A technique is discussed which, when applied
to an iterative procedure for the solution of
an equation, accelerates the rate of convergence if
the iteration converges and induces convergence if
the iteration diverges.  An illustrative example is given.”""")

    print("\nRetrieve docs that contains 'iter':")
    print(idx.getTfsForStem("iter"))
    print("Should include doc 20") 
    
    print("\n###### Testing BinaryWeighter: ###### ")
    bw = modeles.BinaryWeighter(idx)
    print("bw.getDocWeightsForDoc(20):", bw.getDocWeightsForDoc(20))
    print("\nbw.getDocWeightsForStem(\"iter\"):", bw.getDocWeightsForStem("iter"))
    query = stemmer.getTextRepresentation("Convergence of Iterative Processes")
    print("\nbw.getWeightsForQuery(query):", bw.getWeightsForQuery(query))
    

    print("\n###### Testing Vectoriel with BinaryWeighter: ###### ")
    vect = modeles.Vectoriel(idx, bw)
    print("Top 10 document for the query:")
    print(vect.getRanking(query)[-10:])
    
    print("\n###### Testing BinaryWeighter: ###### ")
    tfidfWeighter = modeles.TfidfWeighter(idx)
    print("tfidfWeighter.getDocWeightsForDoc(20):", 
        tfidfWeighter.getDocWeightsForDoc(20))
    print("\ntfidfWeighter.getDocWeightsForStem(\"iter\"):", 
        tfidfWeighter.getDocWeightsForStem("iter"))
    query = stemmer.getTextRepresentation("Convergence of Iterative Processes")
    print("\ntfidfWeighter.getWeightsForQuery(query):", 
        tfidfWeighter.getWeightsForQuery(query))
    

    print("\n###### Testing Vectoriel with TfidfWeighter: ###### ")
    vect = modeles.Vectoriel(idx, tfidfWeighter)
    print("Top 10 document for the query:")
    print(vect.getRanking(query)[-10:])
    
          
    
