#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
@author: Loïc Herbelot
"""

import io
import re


class Query():
    def __init__(self, queryID, text,relevants=None):
        """
        :param queryID:
        :param text:
        :param relevants: Dictionary {id: {"subtheme":int, "score":float}}
        """
        self.id = queryID
        self.text = text
        self.relevants = relevants

    def getID(self):
        return self.id

    def getText(self):
        return self.text

    def getRelevants(self):
        return self.relevants

    def setRelevants(self, rel):
        self.relevants = rel

    def __str__(self):
        return "id="+self.id+"\ntxt="+self.text+"\nrelevances="+str(self.relevants)


class QueryParser:
    def __init__(self, qry, rel):
        """ Constructor
        """
        # open the files and get their lengths
        self.qryFile = open(qry, "r")
        self.qryLen = self.qryFile.seek(0, io.SEEK_END)
        self.qryFile.seek(0)

        self.relFile = open(rel, "r")
        self.relLen = self.relFile.seek(0, io.SEEK_END)
        self.relFile.seek(0)
    
    def __del__(self):
        if (self.qryFile is not None):
            self.qryFile.close()
        if (self.relFile is not None):
            self.relFile.close()
    
    def nextQuery(self):
        # Extract data between start and end tags
        # Call the abstract method "parseData" to construct a Query object
        # Call the abstract method "extractRelevance(queryId)" 
        # to extract the relevant docs and get a dictionary
        # Add this dictionary to the Query object
        raise NotImplementedError

    def getQuery(self, queryText, queryRel):
        raise NotImplementedError


class QueryParserCACM(QueryParser):
    def __init__(self, qryFile, relFile):
        """ Constructor"""
        self.begin = ".I"
        super().__init__(qryFile, relFile)


    def parseRelevance(self, data):
        """ Parse the raw relevances in text to a dictionary
        :return: A dictionary {id(int): {"subtheme":int, "score":float"}} 
        """
        dic = {}
        for line in data.split('\n'):
            if len(line) >1:
                search = re.search("^\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*$", line)
                qryId, docId, subtheme, score = search.groups()
                dic[int(docId)] = {"subtheme":int(subtheme),
                                   "score":float(score)}
        return dic

    def parseQuery(self, data):
        """ Parse the raw query data into a Query object
        .I [id]
        .W
         [text]
        :return: a Query object"""
        idSearch = re.search(".I (\d+)", data)
        if idSearch is None:
            print("Error, can't retrieve the ID of the query in '"+data+"'")
        queryId = idSearch.group(1)

        questionSearch = re.search(".W([\s\S]*?)\.[A-Z]", data)
        if questionSearch is None:
            print("Error, can't retrieve the question of the query in '"+data+"'")
        question = questionSearch.group(1)

        return Query(queryId, question)



    def extractRelevance(self, qryId):
        """ Extract the data from the .rel file"""

        def startsNumber(s, n):
            """Returns whether s starts with n (string)"""
            return re.match("^0*(\d*)", s).group(1) == n

        line = self.relFile.readline()
        while (self.relFile.tell() < self.relLen and 
               not startsNumber(line, qryId)):
#            print(">", line, end='')
            line = self.relFile.readline()
        # if line is None, we have reached the end of the file and 
        # we did not see any start tag.
        if self.relFile.tell() == self.relLen:
            return None
#        print("Found the start:", line)
        queryData = line

#        print("Reading the relevances")
        cursor = self.relFile.tell()
        line = self.relFile.readline()
        while (self.relFile.tell() < self.relLen and 
               startsNumber(line, qryId)) :
            queryData += line
#            print(">", line, end='')
            cursor = self.relFile.tell()
            line = self.relFile.readline()

        # Reposition the cursor before the new start tag
        self.relFile.seek(cursor)
        return queryData


    def extractDataFromQry(self):
        """ Return the data extracted and reposition the cursor in the qry file
        :return: data
        """     

        # Read until the first start tag
        line = self.qryFile.readline()
        while (self.qryFile.tell() < self.qryLen and 
               self.begin not in line) :
#            print(">", line, end='')
            line = self.qryFile.readline()
        # if line is None, we have reached the end of the file and 
        # we did not see any start tag.
        if self.qryFile.tell() == self.qryLen:
            return None
#        print("Found the start:", line)
#        print("Retrieve relevances")
        qryId = re.search("0*(\d+)", line).group(1)
        rels = self.extractRelevance(qryId)
        queryData = line

        # Read line by line until the end tag or a new start tag.
#        print("Reading the data query")
        cursor = self.qryFile.tell()
        line = self.qryFile.readline()
        while (self.qryFile.tell() < self.qryLen and 
               self.begin not in line):
#            print(">", line, end='')        
            queryData += line
            cursor = self.qryFile.tell()
            line = self.qryFile.readline()

        # Reposition the cursor before the new start tag
        self.qryFile.seek(cursor)

        return queryData, rels

    def nextQuery(self):
        queryData, queryRels =  self.extractDataFromQry()
        query = self.parseQuery(queryData)
        query.setRelevants(self.parseRelevance(queryRels))
        return query




if __name__ == "__main__":
    qp = QueryParserCACM("cacm/cacm.qry", "cacm/cacm.rel")
    print("Query:",qp.nextQuery())
    print("Query:",qp.nextQuery())
    print("Query:",qp.nextQuery())