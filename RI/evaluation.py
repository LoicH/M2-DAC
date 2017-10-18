#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
@author: Loïc Herbelot
"""

import io


class Query():
    def __init__(self, queryID, text, relevants):
        self.id = queryID
        self.text = text
        self.relevants = relevants

    def getID(self):
        return self.id

    def getText(self):
        return self.text

    def getRelevants(self):
        return self.relevants


class QueryParser:
    def __init__(self, begin, end=""):
        """ Constructor
        :param begin: Start tag
        """
        self.begin = begin
        self.end   = end
        self.file  = None
        self.fileLen = -1

    def initFile(self,filename):
        self.file = open(filename, "r")
        # Does not cost much:
        self.fileLen = self.file.seek(0, io.SEEK_END)
        self.file.seek(0)
    
    def __del__(self):
        if (self.file is not None):
            self.file.close()
            
    def nextQuery(self):
        # Read until seeing the first start tag
        # print("Searching for the '%s' tag" % self.begin)

        line = self.file.readline()
        while (self.file.tell() < self.fileLen and 
               self.begin not in line) :
            # print(">", line)
            line = self.file.readline()
        # if line is None, we have reached the end of the file and 
        # we did not see any start tag.
        if self.file.tell() == self.fileLen:
            return None
        # print("Found the start:", line)
        queryData = line

        # Read line by line until seeing the end tag or a new start tag.
        # print("Reading the data query")
        cursor = self.file.tell()
        line = self.file.readline()
        while (self.file.tell() < self.fileLen and 
               self.begin not in line and
               (not self.end or self.end not in line)) :
            queryData += line
            cursor = self.file.tell()
            line = self.file.readline()

        # print("Data read:", queryData)
        # Reposition the cursor before the new start tag if
        # we saw an other start tag
        if line is not None:
            self.file.seek(cursor)

        # Return the read query:
        return self.getQuery(queryData)


    def getQuery(self,text):
        return text
        # raise NotImplementedError


# class QueryParserCACM(QueryParser):





if __name__ == "__main__":
    qp = QueryParser(".I")
    qp.initFile("cacm/cacm.qry")
    print("Query:",qp.nextQuery())
    print("Query:",qp.nextQuery())
    print("Query:",qp.nextQuery())