#!/usr/bin/env python2
#encoding:utf-8
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, term

# define wrapper
sparql = SPARQLWrapper("http://data.linkedmdb.org/sparql")

# define query
prefix = """
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
PREFIX oddlinker: <http://data.linkedmdb.org/resource/oddlinker/> 
PREFIX map: <file:/C:/d2r-server-0.4/mapping.n3#> 
PREFIX db: <http://data.linkedmdb.org/resource/> 
PREFIX dbpedia: <http://dbpedia.org/property/> 
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX dc: <http://purl.org/dc/terms/> 
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
PREFIX film: <http://data.linkedmdb.org/resource/film/>
PREFIX all: <http://data.linkedmdb.org/all/>
PREFIX directory: <http://data.linkedmdb.org/directory/>

""";



sparql.setQuery(prefix + """
SELECT *
WHERE { ?director rdf:type movie:director; 
				  movie:director_name ?n ;
				  foaf:made ?movie .
				  
		?movie movie:actor ?actor . 
		?actor movie:actor_name ?n .
		?movie rdfs:label ?movieName .}
""")
sparql.setReturnFormat(JSON)

# execute query
results = sparql.query().convert()
#~ print(results)

# function cp transforms SPARQL variable into URI or Literal
def cp(v):
	if (v["type"]=='uri' or v["type"]=='bnode'):
		return URIRef(v["value"].encode('utf-8'))
	else :
		return Literal(v["value"].encode('utf-8'))

# copy result
g = Graph()
for result in results["results"]["bindings"]:
	print(result)
	vs = cp(result["director"])
	vp = URIRef("foaf:made")
	vo = cp(result["movie"])
	g.add((vs,vp,vo))

# evalute SPARQL query on g
result = g.query(prefix + """
SELECT  ?a ?p ?hasValue 
WHERE { ?a ?p ?hasValue . }
""")

# ecrire resultat dans un fichier csv
print(result.serialize(format="csv"))

# evalute SPARQL query on g
result = g.query(prefix + """
CONSTRUCT { ?a  foaf:made ?hasValue }
WHERE { ?a foaf:made ?hasValue . }
""")

# ecrire resultat dans un fichier turtle
result.serialize(destination="gendata/resultat.ttl",format="n3")


