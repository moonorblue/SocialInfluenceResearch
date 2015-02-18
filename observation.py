from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time





graph=Graph()
rootPath = "/home/ytwen/fbdata/"
counter=0
timeIntervalAll=[]
rawIntervalAll=[]
for i in range(0,367):
    timeIntervalAll.append(0)
for user in listdir(rootPath):
#users = graph.cypher.execute("MATCH (n:User) RETURN n.id")
#for user in users:
    #userID = user['n.id'].encode()
    userID = user
    places = graph.cypher.execute("MATCH (n:User {id:{uid}})-[r:VISITED]->(place) RETURN r.atTime,place.id;",{"uid":userID})
    friends = graph.cypher.execute("MATCH (n:User {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;",{"uid":userID})
    timeInterval = []
    rawInterval = []
    
    for i in range(0,367):
        timeInterval.append(0)
    
    for place in places:
        placeVisitTime = place['r.atTime'].encode()
        placeID = place['place.id']
        
        for friend in friends:
            visitRecords = graph.cypher.execute("MATCH (n:User {id:{friendid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN r.atTime;",{"friendid":friend['friend.id'],"pid":placeID})
            
            for record in visitRecords:
                friendVisitTime = record['r.atTime'].encode()

                if( friendVisitTime > placeVisitTime ):
                    interval = int(float(friendVisitTime)) - int(float(placeVisitTime))
                    toDay = interval/86400
                    rawInterval.append(str(interval))
                    rawIntervalAll.append(str(interval))

                    if(toDay < 366):
                        timeInterval[toDay] = timeInterval[toDay] + 1
                        timeIntervalAll[toDay] = timeIntervalAll[toDay] + 1
                    else:
                        timeInterval[366] = timeInterval[366] + 1
                        timeIntervalAll[366] = timeIntervalAll[366] + 1

    f = open('/home/ytwen/observationData/'+userID,'wb')
    for i in xrange(len(timeInterval)):
        f.write(str(i)+','+str(timeInterval[i])+'\n')
    f.close()

    w = open('/home/ytwen/rawobservationData/'+userID,'wb')
    w.write(json.dumps(rawInterval))
    w.close()

z = open('/home/ytwen/observationData/sumData','wb')
for i in xrange(len(timeIntervalAll)):
    z.write(str(i)+','+str(timeIntervalAll[i])+'\n')
z.close()
