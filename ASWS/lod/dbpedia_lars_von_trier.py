#!/usr/bin/env python
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, term


# create SPARQL Wrapper for dbpedia
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
director = "http://dbpedia.org/resource/Lars_von_Trier"

# create SPARQL query

query = """
PREFIX dbpedia: <http://dbpedia.org/resource/>
SELECT ?dir ?prop ?propVal
WHERE {  bind (<""" + director + """> as ?dir)
         ?dir ?prop ?propVal . } """

print(query)

sparql.setQuery(query)

sparql.setReturnFormat(JSON)

# function cp transforms SPARQL variable into URI or Literal
def cp(v):
    if (v["type"]=='uri' or v["type"]=='bnode'):
        return URIRef(v["value"])
    else :
        return Literal(v["value"]) 


# execute SPARQL query
results = sparql.query().convert()

# copy results into g
g = Graph()
for t in results["results"]["bindings"]:
    vs = cp(t["dir"])
    vp = cp(t["prop"])
    vo = cp(t["propVal"])
    g.add((vs,vp,vo))

# display g
print(g.serialize(format='n3'))

