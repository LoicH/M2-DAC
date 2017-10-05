# -*- coding: utf-8 -*-

""" Created on 28th sep. 2017
@author: Loïc Herbelot
"""

import ParserCACM
import TextRepresenter
import os

class Index(object):
    """ Stores word frequencies among documents """


    def __init__(self, name, out_dir):
        """ Constructor 
        :param name: the name of the index. The index will be 
            stored under [directory]/[name]_{index, inverted}
        :param out_dir: Where to save the index.
        """
        # The name of the index
        self.name = name
        # The path to the index file
        self.indexPath = os.path.join(out_dir, self.name + "_index")
        # The path to the inverted index file
        self.invertedPath = os.path.join(out_dir, self.name + "_inverted")
        # Dictionary {doc: (position in index, len of representation)} 
        self.docs = {}
        # Dict {stem: (position in inverted idx, len of repr.)}
        self.stems = {}
        # Dict {doc: (srcFile, position in src, len)}
        self.docFrom = {}
        #TODO ^
        # The list of all stems by order of adding in inverted index.
        #~ self.vocab = []
        
        
    def indexation(self, corpus, parser, txtRepr):
        """ Create the indexes.
        :param corpus: the path to the files that contains 
            all document informations
        :param parser: The Parser object, must implement nextDocument() 
            method
        :param txtRepr: The TextRepresenter object, must implement
            getTextRepresentation(str) method.
        """ 
        print("Performing the indexation...")
        # The path to the files
        self.corpus = corpus
        self.parser = parser
        self.textRepresenter = txtRepr
        
        self.parser.initFile(self.corpus)
        
        # Build the index of documents and compute the length of stem repre
        print("1st pass: build the index")
        doc = self.parser.nextDocument()
        with open(self.indexPath, "w") as index:
            while doc is not None:
                title = doc.getId()
                #~ print("Parsing doc n°" + title)
                stems = (self.textRepresenter
                            .getTextRepresentation(doc.getText()))
                for stem in stems.keys():
					self.addStem(stem, title)
                stems = [w + ":" + str(n) for (w, n) in stems.items()]
                # the string that will be written:
                toWrite = title + '{'
                toWrite += ','.join(stems) + '}\n'
                self.docs[title] = (index.tell(), len(toWrite))
                
                index.write(toWrite)
                doc = self.parser.nextDocument()
        
        
        # Build the inverted index
        print("2nd pass: build the inverted index")
		self.parser.initFile(self.corpus) # Reset the parser 
        doc = self.parser.nextDocument()
        while doc is not None:
			title = doc.getId()
			print("Parsing doc n°" + title)
			stems = (self.textRepresenter
						.getTextRepresentation(doc.getText()))
			for stem in stems.keys():
					

        
        print("Finished")
        
        
    def writeStem(self, stem, docId):
		"""Write the stem in the inverted index"""
		if self.stems[stem]["pos"] >= 0:  # We already encoutered this stem
			
		else: # New stem
		
    def addStem(self, stem, docId):
		""" Add the stem in self.stems (used in 1st pass)
		:param docId: string
		"""
		if stem in self.stems:
			lenToAdd = len(docId) + 1 # for "docId,"
			self.stems[stem]["len"] += lenToAdd
					
		# Or add the new stem:
		else:
			self.stems[stem] = {"pos": -1,
								"len": len(docId) + 2}
        
    def getTfsForDoc(self, docId):
		""" Return the representation of a given document"""
        (pos, length) = self.docs[docId]
        tfs = None
        with open(self.indexPath, 'r') as index:
            index.seek(pos)
            descr = index.read(length)
            start = descr.find('{')
            stop = descr.find('}')
            descr = descr[start+1:stop]
            # [descr] looks like "word:freq,word:freq"
            freqs = [stem.split(':') for stem in descr.split(',')]
            tfs = {word:int(freq) for (word, freq) in freqs}
        
        return tfs
        
    def getTfsForStem(self, stem):
		"""Return the doc frequencies of a given stem from 
		the inverted index."""
        return None
        
    def getStrDoc(self, doc):
		""" Return the string from where a document came from in the 
		source file""" 
        return None




