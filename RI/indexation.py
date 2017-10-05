#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ParserCACM
import TextRepresenter
import Index

# TODO:
# - rename indexation.py to main
# - change Index.docs to add 'pos' and 'len' support
# - Add line returns to inverted indexes

if __name__ == "__main__":
    cacm_txt = "cacm/cacm.txt"

    idx = Index.Index("cacm", "gendata/")
    idx.indexation("cacm/cacm.txt", ParserCACM.ParserCACM(),
                   TextRepresenter.PorterStemmer())
    print("Retrieve stems for doc 111")
    print(idx.getTfsForDoc("111"))
    
    print("""Should look like "Glossary of Computer Engineering and 
Programming Terminology" """)
                   
    
