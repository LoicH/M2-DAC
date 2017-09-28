#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ParserCACM
import TextRepresenter

def index(corpus, out_file):
	""" Build the index of words in documents 
	:param corpus: The path to the corpus file. 
	:param out_file: The path to the destination file.
	:return: A dict {id: position} to find documents in the
			 output file 
	""" 
	
	parser = ParserCACM.ParserCACM()
	parser.initFile("cacm/cacm.txt")
	doc = parser.nextDocument()
	inverted_idx = []
	docs_position = {}
	stemmer = TextRepresenter.PorterStemmer()
	i=0
	with open(out_file, "wb") as index:
		while doc is not None:
			title = doc.getId()
			docs_position[title] = index.tell()
			stems = stemmer.getTextRepresentation(doc.getText())
			stems = [w + ":" + str(n) for (w, n) in stems.items()]
			
			index.write(title + "{")
			index.write(','.join(stems))
			index.write("}\n")
			doc = parser.nextDocument()
	return docs_position
			
		

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
	
	print("index:")
	docs_pos = index(cacm_txt, "index.txt")
	print(docs_pos)
