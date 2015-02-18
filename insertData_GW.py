from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
from sets import Set

def insertPlace(lon,lat,pID):
    graph.cypher.execute("CREATE (p:GWLPlace {id:{pID},latitude:{lat},longitude:{lon} });",{"lon":lon,"lat":lat,"pID":pID})

def insertCheckinAndPlace(uID,timestamp,lon,lat,pID):
    graph.cypher.execute("MATCH (n:GWLUser {id:{uID}}),(p:GWLPlace {id:{pID}}) CREATE (n)-[r:VISITED {atTime:{timestamp}}]->(p);",{"uID":uID,"timestamp":timestamp,"pID":pID})

def inserUserAndFriendship(uID,fID):
    graph.cypher.execute("MERGE (n:GWUser {id:{uID}})-[r:KNOWS]->(f:GWUser {id:{fID}});",{"uID":uID,"fID":fID})   

graph = Graph()
place = Set([])
#f = open("/home/ytwen/rawdata/gw/Gowalla_edges.txt")
f = open("/home/ytwen/rawdata/gwl/Gowalla_totalCheckins.txt")
for line in f.readlines(): 
    line = line.strip()
    line = line.split()
    #if( len(line) == 2 ):
    #    inserUserAndFriendship(line[0],line[1])
    if( len(line) == 5 ):
        #uID = line[0]
        #timestamp = time.mktime(time.strptime(line[1], '%Y-%m-%dT%H:%M:%SZ'))
        lon = line[2]
        lat = line[3]
        pID = line[4]
        
        if((pID in place) == False):
            insertPlace(lon,lat,pID)
            place.add(pID)  
        #insertCheckinAndPlace(uID,str(timestamp),lon,lat,pID)

graph.cypher.execute("CREATE INDEX ON :GWLPlace(id);")

f = open("/home/ytwen/rawdata/gwl/Gowalla_totalCheckins.txt")
for line in f.readlines():
    line = line.strip()
    line = line.split()
    #if( len(line) == 2 ):
    #    inserUserAndFriendship(line[0],line[1])
    if( len(line) == 5 ):
        uID = line[0]
        timestamp = time.mktime(time.strptime(line[1], '%Y-%m-%dT%H:%M:%SZ'))
        lon = line[2]
        lat = line[3]
        pID = line[4]

        #if((pID in place) == False):
        #    insertPlace(lon,lat,pID)
        #    place.add(pID)
        insertCheckinAndPlace(uID,str(timestamp),lon,lat,pID)
