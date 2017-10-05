#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ParserCACM
import TextRepresenter
import Index

# TODO:
# - change Index.docs to add 'pos' and 'len' support
# - change inverted index construction to add term frequency.

if __name__ == "__main__":
    cacm_txt = "cacm/cacm.txt"

	# Construct the index:
    idx = Index.Index("cacm", "gendata/")
    idx.indexation("cacm/cacm.txt", ParserCACM.ParserCACM(),
                   TextRepresenter.PorterStemmer())
                   
    print("###### A bit of testing: ###### ")
    print("Retrieve stems in doc 19:")
    print(idx.getTfsForDoc("19"))
    print("Should look like “Glossary of Computer Engineering and \
Programming Terminology”")

    print("Retrieve docs that contains “propos”:")
    print(idx.getTfsForStem("propos"))
    print("Should include docs 9, 11 and 14")

	

	
                   
    
