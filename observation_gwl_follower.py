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
    locs = graph.cypher.execute("MATCH (n:GWLUser {id:{uid}})-[:VISITED]->(p:GWLPlace) RETURN p.id;",{"uid":uid})
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
    landl = graph.cypher.execute("MATCH (p:GWLPlace {id:{pid}}) RETURN p.latitude,p.longitude;",{"pid":l})
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
rootPath = "/home/ytwen/observationData_follower_one/gwl"
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
users = graph.cypher.execute("MATCH (n:GWLUser) RETURN n.id")
for user in users:
    userID = user['n.id'].encode()
    #userID = "80"
    if((userID+".csv") in exist or (userID+"_distance") in exist):
        print(str(userID)+" exists, skip.") 
        continue
    mflocation = getMFLocation(userID)
    if(mflocation == False):
        continue    
    #userID = user
    friends = graph.cypher.execute("MATCH (n:GWLUser {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;",{"uid":userID})
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
        visitRecords = graph.cypher.execute("MATCH (n:GWLUser {id:{friendid}})-[r:VISITED]->(p:GWLPlace) RETURN p.category,p.id,r.atTime;",{"friendid":friend['friend.id']})
        isVisit=[]
         
        for record in visitRecords:
            if( record['p.id'] in isVisit):
                break
            else:
                isVisit.append(record['p.id'])
             
            totalRecords = graph.cypher.execute("MATCH (n:GWLUser {id:{friendid}})-[r:VISITED]->(p:GWLPlace {id:{pid}}) RETURN r.atTime ORDER BY r.atTime DESC;",{"friendid":friend['friend.id'], "pid":record['p.id']})
            
            
            
            #if( record['p.category'] in visitType):
            #    visitType[record['p.category']] = visitType[record['p.category']] + 1
            #else:
            #    visitType[record['p.category']] = 1

            
            userVisitRecords = graph.cypher.execute("MATCH (n:GWLUser {id:{userid}})-[r:VISITED]->(p:GWLPlace {id:{pid}}) RETURN r.atTime;",{"userid":userID,"pid":record['p.id']})
            for userVisitRecord in userVisitRecords:
                userVisitTime = float(userVisitRecord['r.atTime'].encode())
                                
                for totalR in totalRecords:
                    if(userVisitTime > float(totalR['r.atTime'].encode())):
                        interval = int(float(userVisitTime)) - int(float(totalR['r.atTime'].encode()))
                        toDay = interval/86400
                        rawInterval.append(str(interval))
                        rawIntervalAll.append(str(interval))

                        locData = graph.cypher.execute("MATCH (p:GWLPlace {id:{pid}}) RETURN p.latitude,p.longitude;",{"pid":record['p.id']})
                        dis = distance_on_unit_sphere(float(mflocation[0]),float(mflocation[1]),float(locData[0]['p.latitude']),float(locData[0]['p.longitude']))
                        
                        distance.append(dis)
                        distanceAll.append(dis)
                                                

                        if(toDay < 366):
                            timeInterval[toDay] = timeInterval[toDay] + 1
                            timeIntervalAll[toDay] = timeIntervalAll[toDay] + 1
                            distanceWithDay[toDay].append(dis)
                            distanceWithDayAll[toDay].append(dis)
                            locationWithDay[toDay].append(record['p.id'].encode())
                            locationWithDayAll[toDay].append(record['p.id'].encode())
                        else:
                            timeInterval[366] = timeInterval[366] + 1
                            timeIntervalAll[366] = timeIntervalAll[366] + 1
                            distanceWithDay[366].append(dis)	
                            distanceWithDayAll[366].append(dis)
                            locationWithDay[366].append(record['p.id'].encode())
                            locationWithDayAll[366].append(record['p.id'].encode())
                        #if( dis in distance):
                        #    distance[dis] = distance[dis] + 1

                        #if( record['p.category'] in visitType):
                        #    visitType[record['p.category']] = visitType[record['p.category']] + 1
                        #else:
                        #    visitType[record['p.category']] = 1
                        
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

    f = open('/home/ytwen/observationData_follower_one/gwl/'+userID+'.csv','wb')
    for i in xrange(len(timeInterval)):
        f.write(str(i)+','+str(timeInterval[i])+','+str(json.dumps(distanceWithDay[i]))+','+str(json.dumps(locationWithDay[i]))+'\n')
    f.close()

    w = open('/home/ytwen/rawobservationData_follower_one/gwl/'+userID,'wb')
    w.write(json.dumps(rawInterval))
    w.close()
    
    d = open('/home/ytwen/observationData_follower_one/gwl/'+userID+'_distance','wb')
    d.write(json.dumps(distance))
    d.close()
    #v = open('/home/ytwen/observationData_follower_one_interest/'+userID+'.csv','wb')
    #total = 0
    #for i in visitType:
    #    total = total + visitType[i]
    #
    #for i in visitType:
    #    v.write(str(i)+","+str(100*(float(visitType[i])/total))+'\n') 
    #v.close() 
    
z = open('/home/ytwen/observationData_follower_one/gwl/sumData.csv','wb')
for i in xrange(len(timeIntervalAll)):
    z.write(str(i)+','+str(timeIntervalAll[i])+','+str(json.dumps(distanceWithDayAll[i]))+','+str(json.dumps(locationWithDayAll[i]))+'\n')
z.close()

y = open('/home/ytwen/observationData_follower_one/gwl/sumData_distance','wb')
y.write(json.dumps(distanceAll))
y.close()

import operator
import matplotlib
matplotlib.use('Agg')
from  matplotlib import pyplot


path = '/home/ytwen/observationData_follower_one/gwl'
followDic = {}
for followdata in listdir(path):
    if ('csv' in followdata) : 
        f = open(path+'/'+followdata)
        sum = 0
        for line in f.readlines():
            sum = sum + int(line.split(',')[1])

        followDic[followdata] = int(sum)

sorted_x = sorted(followDic.items(), key=operator.itemgetter(1),reverse=True)

topk = int(0.2 * len(sorted_x))

for i in xrange(topk+1):
    plt = pyplot
    f = open(path+'/'+sorted_x[i][0])
    datalist = []
    count = 0
    for l in f.readlines():
        if (count == 100):
            break
        datalist.append(l.split(',')[1])
        count = count + 1

    plt.plot(datalist)
    plt.ylabel('follow counts')
    plt.xlabel('days')
    plt.savefig(path+'/'+'Num-'+str(i)+':'+str(sorted_x[i][0])+'.png')
    plt.close()
