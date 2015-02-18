from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
from sets import Set


def insertUserAndFriendship(uID,fID):
    graph.cypher.execute("MATCH (n:GWLUser {id:{uid}}),(f:GWLUser {id:{fid}}) CREATE (n)-[r:KNOWS]->(f) ;",{"uid":uID,"fid":fID})

def insertUser(uID):
    graph.cypher.execute("CREATE (n:GWLUser {id:{uid}});",{"uid":uID})
    
def createIndex():
    graph.cypher.execute("CREATE INDEX ON :GWLUser(id)")

graph = Graph()
f = open("/home/ytwen/rawdata/gwl/Gowalla_edges.txt")
users=Set([])
for line in f.readlines():
    line = line.strip()
    line = line.split()
    if( len(line) == 2 ):
        for i in line:
            if((i in users) == False):
                users.add(i)
                insertUser(i)

f = open("/home/ytwen/rawdata/gwl/Gowalla_edges.txt")
for line in f.readlines():
    line = line.strip()
    line = line.split()
    if( len(line) == 2 ):
        insertUserAndFriendship(line[0],line[1])
