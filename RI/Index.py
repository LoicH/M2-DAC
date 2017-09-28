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
        :param directory: Where to save the index.
        """
        self.name = name
        self.indexPath = os.path.join(out_dir, self.name + "_index")
        self.invertedPath = os.path.join(out_dir, self.name + "_inverted")
        self.docs = {}
        self.stems = {}
        self.docFrom = {}
        
        
    def indexation(self, corpus, parser, txtRepr):
        """ Create the index.
        :param corpus: the path to the fils that contains 
            all document informations
        :param parser: The Parser object, must implement nextDocument() 
            method
        :param txtRepr: The TextRepresenter object, must implement
            getTextRepresentation(str) method.
        """ 
        print("Performing the indexation...")
        self.corpus = corpus
        self.parser = parser
        self.textRepresenter = txtRepr
        
        self.parser.initFile(self.corpus)
        inverted_idx = []
        
        # Iterate over all documents
        doc = self.parser.nextDocument()
        with open(self.indexPath, "w") as index:
            while doc is not None:
                title = doc.getId()
                print("Parsing doc n°" + title)
                stems = (self.textRepresenter
                            .getTextRepresentation(doc.getText()))
                stems = [w + ":" + str(n) for (w, n) in stems.items()]
                # the string that will be written:
                toWrite = title + '{'
                toWrite += ','.join(stems) + '}\n'
                self.docs[title] = (index.tell(), len(toWrite))
                
                index.write(toWrite)
                doc = self.parser.nextDocument()
        print("Finished")
        
        
    def getTfsForDoc(self, docId):
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
        
    def getTfsForStem(self):
        return None
        
    def getStrDoc(self):
        return None




