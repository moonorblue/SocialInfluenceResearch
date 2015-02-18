from py2neo import Graph
import sys
import json



cL=[]

g = Graph()
locs = g.cypher.execute("MATCH (p:Place) Return p.category")
for l in locs:
    category = str(l['p.category'])
    if category not in cL:
      cL.append(category)
      print category
    else:
      continue

cL.sort()
w = open('/home/ytwen/category_fb','w')
w.write(json.dumps(cL))
w.close()


cL=[]

locs = g.cypher.execute("MATCH (p:CAPlace) Return p.category")
for l in locs:
    category = eval(l['p.category'])
    for c in category:
      if len(c) > 1:
        if c not in cL:
          cL.append(c)
          print c
        else:
          continue

cL.sort()
w = open('/home/ytwen/category_CA','w')
w.write(json.dumps(cL))
w.close()