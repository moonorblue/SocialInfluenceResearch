from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
import math
import operator
from multiprocessing.pool import ThreadPool as Pool
# from multiprocessing import Pool

rootPath = "/home/ytwen/observationData_follower_one/v2/GWL"
exist = listdir(rootPath)


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


def calFollow(userID):

    print "Start #:",str(userID)
    if((userID+".csv") in exist or (userID+"_distance") in exist):
        print(str(userID)+" exists, skip.")
        return 0

    mflocation = getMFLocation(userID)
    if(mflocation == False):
        return 0

    friends = graph.cypher.execute("MATCH (n:GWLUser {id:{uid}})-[:KNOWS]->(f:GWLUser) RETURN f.id;",{"uid":userID})
    timeInterval = []
    # rawInterval = []
    distance = []
    distanceWithDay = []
    locationWithDay = []

    for i in range(0,101):
        timeInterval.append(0)
        distanceWithDay.append([])
        locationWithDay.append([])

    for friend in friends:
        visitRecords = graph.cypher.execute("MATCH (n:GWLUser {id:{friendid}})-[r:VISITED]->(p:GWLPlace) RETURN DISTINCT p.id;",{"friendid":friend['f.id']})
        isVisit=[]

        for record in visitRecords:
            if( record['p.id'] in isVisit):
                continue
            else:
                isVisit.append(record['p.id'])

            totalRecords = graph.cypher.execute("MATCH (n:GWLUser {id:{friendid}})-[r:VISITED]->(p:GWLPlace {id:{pid}}) RETURN r.atTime ORDER BY r.atTime DESC;",{"friendid":friend['f.id'], "pid":record['p.id']})
            userVisitRecords = graph.cypher.execute("MATCH (n:GWLUser {id:{userid}})-[r:VISITED]->(p:GWLPlace {id:{pid}}) RETURN r.atTime ORDER BY r.atTime;",{"userid":userID,"pid":record['p.id']})

            flag = False
            for userVisitRecord in userVisitRecords:
                userVisitTime = float(userVisitRecord['r.atTime'])#not sure the order, shouldd from small to big

                for totalR in totalRecords: # timestamp from big to small
                    if(userVisitTime > float(totalR['r.atTime'])):
                        interval = int(float(userVisitTime)) - int(float(totalR['r.atTime']))
                        toDay = interval/86400

                        locData = graph.cypher.execute("MATCH (p:GWLPlace {id:{pid}}) RETURN p.latitude,p.longitude;",{"pid":record['p.id']})
                        dis = distance_on_unit_sphere(float(mflocation[0]),float(mflocation[1]),float(locData[0]['p.latitude']),float(locData[0]['p.longitude']))

                        if(toDay < 101):
                            timeInterval[toDay] = timeInterval[toDay] + 1
                            # timeIntervalAll[toDay] = timeIntervalAll[toDay] + 1
                            distanceWithDay[toDay].append(dis)
                            # distanceWithDayAll[toDay].append(dis)
                            locationWithDay[toDay].append(record['p.id'])
                            # locationWithDayAll[toDay].append(record['p.id'])

                        flag = True
                        break

                if flag == True:
                    break





    f = open('/home/ytwen/observationData_follower_one/v2/GWL/'+userID+'.csv','wb')
    for i in xrange(len(timeInterval)):
        f.write(str(i)+','+str(timeInterval[i])+','+str(json.dumps(distanceWithDay[i]))+','+str(json.dumps(locationWithDay[i]))+'\n')
    f.close()

    w = open('/home/ytwen/rawobservationData_follower_one/v2/GWL/'+userID,'wb')
    # w.write(json.dumps(rawInterval))
    # w.close()

    # d = open('/home/ytwen/observationData_follower_one/v2/GWL/'+userID+'_distance','wb')
    # d.write(json.dumps(distance))
    # d.close()




graph=Graph()
# rootPath = "/home/ytwen/observationData_follower_one/v2/GWL"
# exist = listdir(rootPath)
counter=0
# timeIntervalAll=[]
# rawIntervalAll=[]
# distanceAll=[]
# distanceWithDayAll=[]
# locationWithDayAll=[]






pool_size = 5  # your "parallelness"
pool = Pool()


# for i in range(0,367):
    # timeIntervalAll.append(0)
    # distanceWithDayAll.append([])
    # locationWithDayAll.append([])

# exist = listdir(rootPath)
users = graph.cypher.execute("MATCH (n:GWLUser) RETURN n.id")
usersL = [u['n.id'] for u in users]

# for i in xrange(len(usersL)):
#     userID = usersL[i]
#     if((userID+".csv") in exist or (userID+"_distance") in exist):
#         print(str(userID)+" exists, skip.")
#         usersL.remove(userID)

# for u in usersL:
#     userID = u
#     if((userID+".csv") in exist or (userID+"_distance") in exist):
#         print(str(userID)+" exists, skip.")
#         continue
#     pool.apply_async(calFollow, (u,))
# for user in users:
#     userID = user['n.id']
#     if((userID+".csv") in exist or (userID+"_distance") in exist):
#         print(str(userID)+" exists, skip.")
#         continue
#     print "Start #:",str(userID)
#     # calFollow(userID)
#     pool.apply_async(calFollow, (userID,))
pool.map(calFollow,usersL)
# for item in items:
    # pool.apply_async(worker, (item,))

pool.close()
pool.join()


# z = open('/home/ytwen/observationData_follower_one/v2/GWL/sumData.csv','wb')
# for i in xrange(len(timeIntervalAll)):
    # z.write(str(i)+','+str(timeIntervalAll[i])+','+str(json.dumps(distanceWithDayAll[i]))+','+str(json.dumps(locationWithDayAll[i]))+'\n')
# z.close()

# y = open('/home/ytwen/observationData_follower_one/v2/GWL/sumData_distance','wb')
# y.write(json.dumps(distanceAll))
# y.close()
