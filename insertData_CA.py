from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
import cPickle as pickle
import re

pairDict={}


def savePickle(dic):
     pickle.dump( dic, open( "/home/ytwen/ca.p", "wb" ) )

def loadPickle():
    return pickle.load( open( "/home/ytwen/ca.p", "rb" ) ) 

def insertPlaceData(pID,lat,lon):
    #graph.cypher.execute("MATCH (p:FSPlace {id:{pid}}) SET p.latitude={lat},p.longitude={lon};",{"pid":pID,"lat":lat,"lon":lon})
    graph.cypher.execute("MERGE (p:CAPlace {id:{pid},latitude:{lat},longitude:{lon}});",{"pid":pID,"lat":lat,"lon":lon})

def insertPlaceCategory(pID,category):
    graph.cypher.execute("MATCH (p:CAPlace {id:{pid}}) SET p.category={cat};",{"pid":pID,"cat":category})


def insertCheckinAndPlace(uID,timestamp,pID,cID):
    #graph.cypher.execute("MERGE (n:FSUser {id:{uID}})-[r:VISITED {id:{cID},atTime:{timestamp}}]->(p:FSPlace {id:{pID}});",{"uID":uID,"cID":cID,"timestamp":timestamp,"pID":pID})
    graph.cypher.execute("MERGE (n:FSUser {id:{uID}}) MERGE (p:FSPlace {id:{pID}}) CREATE (n)-[r:VISITED {id:{cID},atTime:{timestamp}}]->(p);",{"uID":uID,"cID":cID,"timestamp":timestamp,"pID":pID})

def insertCheckin(uID,timestamp,pID):
    graph.cypher.execute("MATCH (n:CAUser {id:{uID}}),(p:CAPlace {id:{pID}}) CREATE (n)-[r:VISITED {atTime:{timestamp}}]->(p);",{"uID":uID,"timestamp":timestamp,"pID":pID})

def insertCheckinWithId(uID,timestamp,pID,cID):
    graph.cypher.execute("MATCH (n:CAUser {id:{uID}})-[r:VISITED {atTime:{timestamp}}]->(p:CAPlace {id:{pID}}) SET r.id = {cid};",{"uID":uID,"timestamp":timestamp,"pID":pID,"cid":str(cID)})

def insertUser(uID):
    graph.cypher.execute("MERGE (n:CAUser {id:{uID}});",{"uID":uID})

def insertFriendship(uID,fID):
    graph.cypher.execute("MATCH (n:CAUser {id:{uID}}),(f:CAUser {id:{fID}})  MERGE (n)-[r:KNOWS]->(f);",{"uID":uID,"fID":fID})   
    

def insertRating(uID,pID,rating):
    graph.cypher.execute("MATCH (n:FSUser {id:{uID}}),(p:FSPlace {id:{pID}}) CREATE (n)-[r:RATES {rating:{rate}}]->(p);",{"uID":uID,"pID":pID,"rate":rating})



def MonthToNum(mon):
    if( mon == 'Jan' ):
        return '01'
    elif( mon == 'Feb' ):
        return '02'
    elif( mon == 'Mar' ):
        return '03'
    elif( mon == 'Apr'):
        return '04'
    elif( mon == 'May'):
        return '05'
    elif( mon == 'Jun'):
        return '06'
    elif( mon == 'Jul'):
        return '07'
    elif( mon == 'Aug'):
        return '08'
    elif( mon == 'Sep'):
        return '09'
    elif( mon == 'Oct'):
        return '10'
    elif( mon == 'Nov'):
        return '11'
    elif( mon == 'Dec'):
        return '12'

graph = Graph()

f=open('/home/ytwen/CA Dataset/checkin_CA_venues.txt')
# f=open('/home/ytwen/CA Dataset/fs_friendship_CA.txt')
flag = False
count = 1
#pairDict = loadPickle()
for l in f.readlines():
    if( flag ):
        #print repr(l)

        #Checkin part
        m=re.match('(.*)\t(.*)\t(.*)\t(\{.*\})\t(\{.*\})\r\n',l)
        #1\tSat Jul 30 20:15:24 +0000 2011\t1\t{40.731354990929475,-74.00363118575608,New York,NY,United States}\t{Food,}\r\n

        uid = str(m.group(1))
        # insertUser(uid)

        pid = str(m.group(3))
        # loc = m.group(4).strip('{').strip('}').split(',') #lat=loc[0] lon=loc[1]
        # insertPlaceData(pid,loc[0],loc[1])

        # categories = m.group(5).strip('{').strip('}').split(',')
        # insertPlaceCategory(pid,json.dumps(categories))
        
        timelist = m.group(2).split(' ')
        timeData = timelist[5]+'-'+MonthToNum(timelist[1])+'-'+timelist[2]+' '+timelist[3]
        timestamp = time.mktime(time.strptime(timeData, '%Y-%m-%d %H:%M:%S'))
        # insertCheckin(uid,timestamp,pid)
        insertCheckinWithId(uid,timestamp,pid,count)

        count += 1

        #Friendship part
        # s = l.strip('\r\n').split(',')
        # insertFriendship(str(s[0]),str(s[1]))


    
    flag = True     
#w.close()        
