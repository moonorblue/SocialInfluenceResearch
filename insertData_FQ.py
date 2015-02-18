from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
import cPickle as pickle
from copy import deepcopy
from py2neo.packages.httpstream import http
http.socket_timeout = 300


def savePickle(dic):
    pickle.dump( dic, open( "/home/ytwen/fs_n.p", "wb" ) )

def loadPickle():
    return pickle.load( open( "/home/ytwen/fs_n.p", "rb" ) )

def insertPlaceData(pID,lat,lon):
    #graph.cypher.execute("MATCH (p:FSPlace {id:{pid}}) SET p.latitude={lat},p.longitude={lon};",{"pid":pID,"lat":lat,"lon":lon})
    graph.cypher.execute("MERGE (p:FSPlace {id:{pid},latitude:{lat},longitude:{lon}});",{"pid":pID,"lat":lat,"lon":lon})
def insertCheckinAndPlace(uID,timestamp,pID,cID):
    #graph.cypher.execute("MERGE (n:FSUser {id:{uID}})-[r:VISITED {id:{cID},atTime:{timestamp}}]->(p:FSPlace {id:{pID}});",{"uID":uID,"cID":cID,"timestamp":timestamp,"pID":pID})
    graph.cypher.execute("MATCH (p:FSPlace {id:{pID}}),(n:FSUser {id:{uID}}) CREATE (n)-[r:VISITED {id:{cID},atTime:{timestamp}}]->(p);",{"uID":uID,"cID":cID,"timestamp":timestamp,"pID":pID})


def insertUser(uID):
    graph.cypher.execute("MERGE (n:FSUser {id:{uID}});",{"uID":uID})

def insertFriendship(uID,fID):
    graph.cypher.execute("MATCH (n:FSUser {id:{uID}}),(f:FSUser {id:{fID}})  CREATE (n)-[r:KNOWS]->(f);",{"uID":uID,"fID":fID})


def insertRating(uID,pID,rating):
    graph.cypher.execute("MATCH (n:FSUser {id:{uID}}),(p:FSPlace {id:{pID}}) CREATE (n)-[r:RATES {rating:{rate}}]->(p);",{"uID":uID,"pID":pID,"rate":rating})

def saveMarker(num):
    w = open('/home/ytwen/fs_c.marker','w')
    w.write(str(num))
    w.close()

graph = Graph()
f=open("/home/ytwen/rawdata/fs/checkins.dat")
# f=open("/home/ytwen/rawdata/fs/socialgraph.dat")
#f=open("/home/ytwen/rawdata/fs/ratings.dat")
#w = open("/home/ytwen/fqdata",'wb')
# f=open("/home/ytwen/rawdata/fs/venues.dat")
# pairDict = loadPickle()

try:
    w = open('/home/ytwen/fs_c.marker')
    print '#############################'
    print 'Exists marker file, set count from marker'
    for i in w:
        marker = int(i)
        print 'Marker sets as :',i
except:
    print 'NO marker file, starts from 0'
    count = 0
    marker = 0


count = 0
flag = False
for l in f.readlines():
    if( count > 0 and count > marker ):

        if( flag == False ):
            print ''
            print 'Start inserting checkins'
            flag = True

        # l = l.translate(None,"|")
        l = l.split('|')
        if (len(l) < 3):
            continue
        else:
            # pid = l[0].strip()
            # lat = l[1].strip()
            # lon = l[2].strip()
            # insertPlaceData(pid,lat,lon)
            # print pid,lat,lon
            cid = l[0].strip()
            uid = l[1].strip()
            pid = l[2].strip()
            timestamp = time.mktime(time.strptime(l[5].strip('\n'), ' %Y-%m-%d %H:%M:%S'))
            # insertFriendship(uid,fid)
            insertCheckinAndPlace(uid,timestamp,pid,cid)
            saveMarker(count)
            #print process
            if(count / 100000 >= 1 and count % 100000 == 0):
                print '#:',str(count)

    count = count + 1



