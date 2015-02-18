from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
import math
import operator


def getMFLocation(uid):
    locs = graph.cypher.execute("MATCH (n:User {id:{uid}})-[:VISITED]->(p:Place) RETURN p.id;",{"uid":uid})
    locDic = {}
    if(len(locs) == 0):
        return False

    for loc in locs:
        lid = loc['p.id']
        if( lid in locDic):
            locDic[lid] = locDic[lid] + 1
        else:
            locDic[lid] = 0
    sorted_dic = sorted(locDic.items(), key=operator.itemgetter(1), reverse = True)
    l = sorted_dic[0][0]
    landl = graph.cypher.execute("MATCH (p:Place {id:{pid}}) RETURN p.latitude,p.longitude;",{"pid":l})
    for x in landl:
        return x['p.latitude'],x['p.longitude']
 
def distance_on_unit_sphere(lat1, long1, lat2, long2):
    #print("#### "+str(lat1)+" "+str(long1)+" "+str(lat2)+" "+str(long2)) 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = round((math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2)),10)

   
    arc = math.acos( cos )
    
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc*6373


graph=Graph()
rootPath = "/home/ytwen/observationData_follower_one/v2/FB"
counter=0
timeIntervalAll=[]
rawIntervalAll=[]
distanceAll=[]
distanceWithDayAll=[]
locationWithDayAll=[]
for i in range(0,367):
    timeIntervalAll.append(0)
    distanceWithDayAll.append([])
    locationWithDayAll.append([])
#for user in listdir(rootPath):
exist = listdir(rootPath)
users = graph.cypher.execute("MATCH (n:User) RETURN n.id")
for user in users:
    userID = user['n.id']
    #userID = "80"
    if((userID+".csv") in exist or (userID+"_distance") in exist):
        print(str(userID)+" exists, skip.") 
        continue
    mflocation = getMFLocation(userID)
    if(mflocation == False):
        continue    
    #userID = user
    friends = graph.cypher.execute("MATCH (n:User {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;",{"uid":userID})
    #places = graph.cypher.execute("MATCH (n:User {id:{uid}})-[r:VISITED]->(place) RETURN r.atTime,place.id;",{"uid":userID})
    #friends = graph.cypher.execute("MATCH (n:User {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;",{"uid":userID})
    timeInterval = []
    rawInterval = []
    distance = []
    distanceWithDay = []
    locationWithDay = []
    #visitType={}   
    for i in range(0,367):
        timeInterval.append(0)
        distanceWithDay.append([])
        locationWithDay.append([])

    for friend in friends:
        visitRecords = graph.cypher.execute("MATCH (n:User {id:{friendid}})-[r:VISITED]->(p:Place) RETURN DISTINCT p.id;",{"friendid":friend['friend.id']})
        isVisit=[]
         
        for record in visitRecords:
            if( record['p.id'] in isVisit):
                continue
            else:
                isVisit.append(record['p.id'])
             
            totalRecords = graph.cypher.execute("MATCH (n:User {id:{friendid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN r.atTime ORDER BY r.atTime DESC;",{"friendid":friend['friend.id'], "pid":record['p.id']})
                        
            userVisitRecords = graph.cypher.execute("MATCH (n:User {id:{userid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN r.atTime ORDER BY r.atTime;",{"userid":userID,"pid":record['p.id']})
            #userVisitRecords = graph.cypher.execute("MATCH (n:User {id:{userid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN r.atTime ORDER BY r.atTime AESC;",{"userid":userID,"pid":record['p.id']})

            flag = False
            for userVisitRecord in userVisitRecords:
                userVisitTime = float(userVisitRecord['r.atTime'])#not sure the order, shouldd from small to big
                                
                for totalR in totalRecords: # timestamp from big to small
                    if(userVisitTime > float(totalR['r.atTime'])):
                        interval = int(float(userVisitTime)) - int(float(totalR['r.atTime']))
                        toDay = interval/86400
                        rawInterval.append(str(interval))
                        rawIntervalAll.append(str(interval))

                        locData = graph.cypher.execute("MATCH (p:Place {id:{pid}}) RETURN p.latitude,p.longitude;",{"pid":record['p.id']})
                        if locData[0]['p.latitude'] == 'NONE':
                            print record['p.id']," : None location data, skip."
                            break

                        dis = distance_on_unit_sphere(float(mflocation[0]),float(mflocation[1]),float(locData[0]['p.latitude']),float(locData[0]['p.longitude']))
                        
                        distance.append(dis)
                        distanceAll.append(dis)
                                                

                        if(toDay < 366):
                            timeInterval[toDay] = timeInterval[toDay] + 1
                            timeIntervalAll[toDay] = timeIntervalAll[toDay] + 1
                            distanceWithDay[toDay].append(dis)
                            distanceWithDayAll[toDay].append(dis)
                            locationWithDay[toDay].append(record['p.id'])
                            locationWithDayAll[toDay].append(record['p.id'])
                        else:
                            timeInterval[366] = timeInterval[366] + 1
                            timeIntervalAll[366] = timeIntervalAll[366] + 1
                            distanceWithDay[366].append(dis)	
                            distanceWithDayAll[366].append(dis)
                            locationWithDay[366].append(record['p.id'])
                            locationWithDayAll[366].append(record['p.id'])
                        flag = True
                        break 

                if flag == True:
                    break





    f = open('/home/ytwen/observationData_follower_one/v2/FB/'+userID+'.csv','wb')
    for i in xrange(len(timeInterval)):
        f.write(str(i)+','+str(timeInterval[i])+','+str(json.dumps(distanceWithDay[i]))+','+str(json.dumps(locationWithDay[i]))+'\n')
    f.close()

    w = open('/home/ytwen/rawobservationData_follower_one/v2/FB/'+userID,'wb')
    w.write(json.dumps(rawInterval))
    w.close()
    
    d = open('/home/ytwen/observationData_follower_one/v2/FB/'+userID+'_distance','wb')
    d.write(json.dumps(distance))
    d.close()

    
z = open('/home/ytwen/observationData_follower_one/v2/FB/sumData.csv','wb')
for i in xrange(len(timeIntervalAll)):
    z.write(str(i)+','+str(timeIntervalAll[i])+','+str(json.dumps(distanceWithDayAll[i]))+','+str(json.dumps(locationWithDayAll[i]))+'\n')
z.close()

y = open('/home/ytwen/observationData_follower_one/v2/FB/sumData_distance','wb')
y.write(json.dumps(distanceAll))
y.close()
