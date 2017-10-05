#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ParserCACM
import TextRepresenter
import Index

if __name__ == "__main__":
    cacm_txt = "cacm/cacm.txt"
    #~ parser = ParserCACM.ParserCACM()
    #~ parser.initFile(cacm_txt)
    #~ doc = parser.nextDocument()
    #~ print("Doc:")
    #~ print(doc)
    #~ stemmer = TextRepresenter.PorterStemmer()
    #~ print("Stem: ")
    #~ print(stemmer.getTextRepresentation("""Now that you have
    #~ learned the rudiments of Unicode, we can look at 
    #~ Python’s Unicode features."""))
    
    #~ print("index:")
    #~ docs_pos = index(cacm_txt, "index.txt")
    #~ print(docs_pos)
    idx = Index.Index("cacm", "gendata/")
    idx.indexation("cacm/cacm.txt", ParserCACM.ParserCACM(),
                   TextRepresenter.PorterStemmer())
    #~ print("Retrieve stems for doc 111")
    #~ print(idx.getTfsForDoc("111"))
    
    #~ print("""Should look like "{scale:1,reliabl:1,appli:1,basic:1,raphson:1,recommend:2,invers:1,rapid:1,newton:1,high:1,shown:1
#~ ,programm:1,solut:1,exampl:1,pitfal:1,rule:1,applic:1,techniqu:2,equat:2,degre:1,present:1,procedur:
#~ 1,illustr:1,accuraci:1,converg:1,realiz:1,ellenberg:1,polynomial:2,bairstow:1,comput:1,circumv:1,gre
#~ at:1,iter:1,root:1,numer:3}" """)
                   
    
