from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time


graph=Graph()
alldata = graph.cypher.execute("MATCH (n:User)-[r:VISITED]->(p:Place) RETURN n.id,p.id,rid;")


