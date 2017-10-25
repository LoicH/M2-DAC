#!/usr/bin/env python
from rdflib import Graph

# read graph from file into src
src = Graph()
src.parse('lod/directors.ttl', format='n3')

# print src
print("******** src:")
print(src.serialize(format='n3'))

# filter triple and copy into dest
dest=Graph()
for s,p,o in src:
  print(o.encode('utf-8'), o.encode('utf-8') == b"Lars von Trier")
  if (o.encode('utf-8') == b"Lars von Trier"):
      dest.add((s,p,o))

print(dest)
for s,p,o in dest:
  print(s.encode('utf-8'),p.encode('utf-8'),o.encode('utf-8'))

# print dest
print("******** dest:")
print(dest.serialize(format='n3'))
