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
    friends = graph.cypher.execute("MATCH (n:User {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;",{"uid":userID})
    #places = graph.cypher.execute("MATCH (n:User {id:{uid}})-[r:VISITED]->(place) RETURN r.atTime,place.id;",{"uid":userID})
    #friends = graph.cypher.execute("MATCH (n:User {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;",{"uid":userID})
    timeInterval = []
    rawInterval = []
    visitType={}   
    for i in range(0,367):
        timeInterval.append(0)
    

    for friend in friends:
        visitRecords = graph.cypher.execute("MATCH (n:User {id:{friendid}})-[r:VISITED]->(p:Place) RETURN p.category,p.id,r.atTime;",{"friendid":friend['friend.id']})
        isVisit=[]
         
        for record in visitRecords:
            if( record['p.id'] in isVisit):
                break
            else:
                isVisit.append(record['p.id'])
             
            totalRecords = graph.cypher.execute("MATCH (n:User {id:{friendid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN r.atTime ORDER BY r.atTime DESC;",{"friendid":friend['friend.id'], "pid":record['p.id']})
            
            
            
            #if( record['p.category'] in visitType):
            #    visitType[record['p.category']] = visitType[record['p.category']] + 1
            #else:
            #    visitType[record['p.category']] = 1

            
            userVisitRecords = graph.cypher.execute("MATCH (n:User {id:{userid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN r.atTime;",{"userid":userID,"pid":record['p.id']})
            for userVisitRecord in userVisitRecords:
                userVisitTime = float(userVisitRecord['r.atTime'].encode())
                                
                for totalR in totalRecords:
                    if(userVisitTime > float(totalR['r.atTime'].encode())):
                        interval = int(float(userVisitTime)) - int(float(totalR['r.atTime'].encode()))
                        toDay = interval/86400
                        rawInterval.append(str(interval))
                        rawIntervalAll.append(str(interval))

                        if(toDay < 366):
                            timeInterval[toDay] = timeInterval[toDay] + 1
                            timeIntervalAll[toDay] = timeIntervalAll[toDay] + 1
                        else:
                            timeInterval[366] = timeInterval[366] + 1
                            timeIntervalAll[366] = timeIntervalAll[366] + 1
                        
                        if( record['p.category'] in visitType):
                            visitType[record['p.category']] = visitType[record['p.category']] + 1
                        else:
                            visitType[record['p.category']] = 1
                        
                        break 

                #if(userVisitTime > friendVisitTime):
                #    interval = int(float(userVisitTime)) - int(float(friendVisitTime))
                #    toDay = interval/86400
                #    rawInterval.append(str(interval))
                #    rawIntervalAll.append(str(interval))

                #    if(toDay < 366):
                #        timeInterval[toDay] = timeInterval[toDay] + 1
                #        timeIntervalAll[toDay] = timeIntervalAll[toDay] + 1
                #    else:
                #        timeInterval[366] = timeInterval[366] + 1
                #        timeIntervalAll[366] = timeIntervalAll[366] + 1



#    for place in places:
#        placeVisitTime = place['r.atTime'].encode()
#        placeID = place['place.id']
        
#        for friend in friends:
#            visitRecords = graph.cypher.execute("MATCH (n:User {id:{friendid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN r.atTime;",{"friendid":friend['friend.id'],"pid":placeID})
            
#            for record in visitRecords:
#               friendVisitTime = record['r.atTime'].encode()

#                if( friendVisitTime > placeVisitTime ):
#                    interval = int(float(friendVisitTime)) - int(float(placeVisitTime))
#                    toDay = interval/86400
#                    rawInterval.append(str(interval))
#                   rawIntervalAll.append(str(interval))

#                    if(toDay < 366):
#                        timeInterval[toDay] = timeInterval[toDay] + 1
#                        timeIntervalAll[toDay] = timeIntervalAll[toDay] + 1
#                    else:
#                        timeInterval[366] = timeInterval[366] + 1
#                        timeIntervalAll[366] = timeIntervalAll[366] + 1

    f = open('/home/ytwen/observationData_follower_one/'+userID+'.csv','wb')
    for i in xrange(len(timeInterval)):
        f.write(str(i)+','+str(timeInterval[i])+'\n')
    f.close()

    w = open('/home/ytwen/rawobservationData_follower_one/'+userID,'wb')
    w.write(json.dumps(rawInterval))
    w.close()

    v = open('/home/ytwen/observationData_follower_one_interest/'+userID+'.csv','wb')
    total = 0
    for i in visitType:
        total = total + visitType[i]

    for i in visitType:
        v.write(str(i)+","+str(100*(float(visitType[i])/total))+'\n') 
    v.close() 
    
z = open('/home/ytwen/observationData_follower_one/sumData.csv','wb')
for i in xrange(len(timeIntervalAll)):
    z.write(str(i)+','+str(timeIntervalAll[i])+'\n')
z.close()
