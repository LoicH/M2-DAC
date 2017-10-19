#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ParserCACM
import TextRepresenter
import indexation
import modeles
from query import QueryParserCACM
import evaluation

if __name__ == "__main__":
    cacm_txt = "cacm_sample/cacm.txt"

    # Construct the index:
    idx = indexation.Index("cacm", "gendata/")
    stemmer = TextRepresenter.PorterStemmer()
    idx.indexation(cacm_txt, ParserCACM.ParserCACM(),
                   stemmer)

    print("\n###### A bit of testing: ###### ")
    print("Retrieve stems in doc 46:")
    print(idx.getTfsForDoc(46))
    print("""Should look like
    “Multiprogramming STRETCH: Feasibility Considerations
    .W
    The tendency towards increased parallelism in
    computers is noted.  Exploitation of this parallelism
    presents a number of new problems in machine design
    and in programming systems.”""")

    print("\nRetrieve docs that contains 'logic':")
    print(idx.getTfsForStem("logic"))
    print("Should include doc 63 and 46")

    print("\n###### Testing BinaryWeighter: ###### ")
    bw = modeles.BinaryWeighter(idx)
    print("bw.getDocWeightsForDoc(46):", bw.getDocWeightsForDoc(46))
    print("\nbw.getDocWeightsForStem(\"logic\"):", bw.getDocWeightsForStem("logic"))
    query = stemmer.getTextRepresentation("parallelism in programming")
    print("\nbw.getWeightsForQuery(query):", bw.getWeightsForQuery(query))


    print("\n###### Testing Vectoriel with BinaryWeighter: ###### ")
    vect = modeles.Vectoriel(idx, bw)
    print("Top 10 document for the query:")
    print(vect.getRanking(query)[:10])

    print("\n###### Testing BinaryWeighter: ###### ")
    tfidfWeighter = modeles.TfidfWeighter(idx)
    print("tfidfWeighter.getDocWeightsForDoc(46):",
        tfidfWeighter.getDocWeightsForDoc(46))
    print("\ntfidfWeighter.getDocWeightsForStem(\"logic\"):",
        tfidfWeighter.getDocWeightsForStem("logic"))
    q = stemmer.getTextRepresentation("parallelism in programming")
    print("\ntfidfWeighter.getWeightsForQuery(query):",
        tfidfWeighter.getWeightsForQuery(q))


    print("\n###### Testing Vectoriel with TfidfWeighter: ###### ")
    vect = modeles.Vectoriel(idx, tfidfWeighter)
    print("Top 10 document for the query:")
    print(vect.getRanking(q)[:10])

    print("\n###### Testing QueryParserCACM: ###### ")
    qp = QueryParserCACM("cacm_sample/cacm.qry", "cacm_sample/cacm.rel")
    query = qp.nextQuery()
    print("Display found queries:")
    while query is not None:
        print(query)
        print(20*'-')
        query = qp.nextQuery()

    print("\n###### Testing evaluation.PrecisionRecallMeasure: ###### ")
    # irlist = evaluation.IRList()
