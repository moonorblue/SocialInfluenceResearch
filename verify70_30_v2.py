from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
import cPickle as pickle
from copy import deepcopy
import sys
import re
import operator
import math
from py2neo.packages.httpstream import http
http.socket_timeout = 9999


def getMFLocation(uid):
    if(datasetName == ''):
        locs = graph.cypher.execute("MATCH (n:User {id:{uid}})-[:VISITED]->(p:Place) RETURN p.id;", {"uid": uid})
    elif(datasetName == 'FS'):
        locs = graph.cypher.execute("MATCH (n:FSUser {id:{uid}})-[:VISITED]->(p:FSPlace) RETURN p.id;", {"uid": uid})
    elif(datasetName ==  'GWL'):
        locs = graph.cypher.execute("MATCH (n:GWLUser {id:{uid}})-[:VISITED]->(p:GWLPlace) RETURN p.id;", {"uid": uid})
    elif(datasetName == 'CA'):
        locs = graph.cypher.execute("MATCH (n:CAUser {id:{uid}})-[:VISITED]->(p:CAPlace) RETURN p.id;", {"uid": uid})

    locDic = {}
    if(len(locs) == 0):
        return False

    for loc in locs:
        lid = loc['p.id']
        if(lid in locDic):
            locDic[lid] = locDic[lid] + 1
        else:
            locDic[lid] = 0
    sorted_dic = sorted(
        locDic.items(), key=operator.itemgetter(1), reverse=True)
    l = sorted_dic[0][0]

    if(datasetName == ''):
        landl = graph.cypher.execute("MATCH (p:Place {id:{pid}}) RETURN p.latitude,p.longitude;", {"pid": l})
    elif(datasetName == 'FS'):
        landl = graph.cypher.execute("MATCH (p:FSPlace {id:{pid}}) RETURN p.latitude,p.longitude;", {"pid": l})
    elif(datasetName ==  'GWL'):
        landl = graph.cypher.execute("MATCH (p:GWLPlace {id:{pid}}) RETURN p.latitude,p.longitude;", {"pid": l})
    elif(datasetName == 'CA'):
        landl = graph.cypher.execute("MATCH (p:CAPlace {id:{pid}}) RETURN p.latitude,p.longitude;", {"pid": l})

    for x in landl:
        return x['p.latitude'], x['p.longitude']


def distance_on_unit_sphere(lat1, long1, lat2, long2):

    degrees_to_radians = math.pi / 180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians

    # theta = longitude
    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = round((math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2)), 10)

    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc * 6373


# get top 10%
def getTop10User(dataset):
    if(dataset == ''):
        dirName = 'fb'
    elif(dataset == 'FS'):
        dirName = 'fs'
    elif(dataset == 'GWL'):
        dirName = 'gwl'
    elif(dataset == 'CA'):
        dirName = 'CA'

    path = '/home/ytwen/observationData_follower_one/' + dirName
    followDic = {}
    disDic = {}
    sumCount = []
    timelist = []
    dislist = []

    for i in range(0, 100):
        sumCount.append(0)

    for followdata in listdir(path):
        if (followdata == 'sumData.csv'):
            continue
        if ('.png' in followdata):
            continue
        if ('distance' in followdata):
            continue
        # print followdata
        f = open(path + '/' + followdata)
        followCount = 0
        for line in f.readlines():

             m = re.match('(.*)\,(.*)\,(\[.*\])\,(\[.*\])', line)

             if m is not None:
                 if (int(m.group(1)) > 99):
                     break

                 sumCount[int(m.group(1))] = sumCount[
                              int(m.group(1))] + int(m.group(2))

                 followCount = followCount + int(m.group(2))

                 disdata = json.loads(m.group(3))


        if(followCount > 0):
            followDic[followdata] = int(followCount)

    sorted_x = sorted(
        followDic.items(), key=operator.itemgetter(1), reverse=True)
    rangelimit = int(0.1 * len(sorted_x))

    newlist = []
    for i in xrange(rangelimit + 1):
      newlist.append(sorted_x[i][0])

    return newlist




def getPeriodmarker(uid):
    if(datasetName == ''):
        q = graph.cypher.execute("MATCH (n:User {id:{uid}})-[r:VISITED]->(p:Place) RETURN max(r.atTime),min(r.atTime)",{"uid":uid})
    elif(datasetName == 'FS'):
        q = graph.cypher.execute("MATCH (n:FSUser {id:{uid}})-[r:VISITED]->(p:FSPlace) RETURN max(r.atTime),min(r.atTime)",{"uid":uid})
    elif(datasetName ==  'GWL'):
        q = graph.cypher.execute("MATCH (n:GWLUser {id:{uid}})-[r:VISITED]->(p:GWLPlace) RETURN max(r.atTime),min(r.atTime)",{"uid":uid})
    elif(datasetName == 'CA'):
        q = graph.cypher.execute("MATCH (n:CAUser {id:{uid}})-[r:VISITED]->(p:CAPlace) RETURN max(r.atTime),min(r.atTime)",{"uid":uid})


    endTime = float(q[0]['max(r.atTime)'])
    startTime = float(q[0]['min(r.atTime)'])

    periodmarker = startTime+0.7*(endTime - startTime)

    return periodmarker



def getGlobalPeriodmarker():
    if(datasetName == ''):
        q = graph.cypher.execute("MATCH (n:User )-[r:VISITED]->(p:Place) RETURN max(r.atTime),min(r.atTime)")
    elif(datasetName == 'FS'):
        q = graph.cypher.execute("MATCH (n:FSUser)-[r:VISITED]->(p:FSPlace) RETURN max(r.atTime),min(r.atTime)")
    elif(datasetName ==  'GWL')
        q = graph.cypher.execute("MATCH (n:GWLUser)-[r:VISITED]->(p:GWLPlace) RETURN max(r.atTime),min(r.atTime)")
    elif(datasetName == 'CA'):
        q = graph.cypher.execute("MATCH (n:CAUser)-[r:VISITED]->(p:CAPlace) RETURN max(r.atTime),min(r.atTime)")


    endTime = float(q[0]['max(r.atTime)'])
    startTime = float(q[0]['min(r.atTime)'])


    periodmarker = startTime+0.7*(endTime - startTime)

    return periodmarker





if(len(sys.argv)>1):
    datasetName = sys.argv[1]
else:
    datasetName = ''



graph = Graph()
rootPath = "/home/ytwen/observationData_follower_one/" + datasetName

print "# Start getting periodmarker"
period_marker = getGlobalPeriodmarker


print "# Get periodmarker:",str(period_marker)
print "###########################################"
print "# Start getting Top10Users"

users = getTop10User(datasetName)
print "# Get Top10Users"
print "###########################################"
print "# Start calculating following relationship"

results = []
for user in users:
    userID = user.strip('.csv')
    print userID
    mflocation = getMFLocation(userID)
    if(mflocation == False):
        continue
    if(datasetName == ''):
        friends = graph.cypher.execute("MATCH (n:User {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;", {"uid": userID})
    elif(datasetName == 'FS'):
        friends = graph.cypher.execute("MATCH (n:FSUser {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;", {"uid": userID})
    elif(datasetName ==  'GWL'):
        friends = graph.cypher.execute("MATCH (n:GWLUser {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;", {"uid": userID})
    elif(datasetName == 'CA'):
        friends = graph.cypher.execute("MATCH (n:CAUser {id:{uid}})-[:KNOWS]->(friend) RETURN friend.id;", {"uid": userID})



    userfollowData = []

    for friend in friends:
        if(datasetName == ''):
            visitRecords = graph.cypher.execute("MATCH (n:User {id:{friendid}})-[r:VISITED]->(p:Place) RETURN p.category,p.id,r.atTime;", {"friendid": friend['friend.id']})
        elif(datasetName == 'FS'):
            visitRecords = graph.cypher.execute("MATCH (n:FSUser {id:{friendid}})-[r:VISITED]->(p:FSPlace) RETURN p.category,p.id,r.atTime;", {"friendid": friend['friend.id']})
        elif(datasetName ==  'GWL'):
            visitRecords = graph.cypher.execute("MATCH (n:GWLUser {id:{friendid}})-[r:VISITED]->(p:GWlPlace) RETURN p.category,p.id,r.atTime;", {"friendid": friend['friend.id']})
        elif(datasetName == 'CA'):
            visitRecords = graph.cypher.execute("MATCH (n:CAUser {id:{friendid}})-[r:VISITED]->(p:CAPlace) RETURN p.category,p.id,r.atTime;", {"friendid": friend['friend.id']})

        isVisit = {}

        fid = friend['friend.id']
        pids = []
        distances = []
        days = []
        categorys = []
        visiteT = []

        for record in visitRecords:
            # check if p.id is followed
            if(record['p.id'] in isVisit):
                break
            else:
                isVisit[record['p.id']] = 1
            # get all visit records by friend of p.id, ordered by time
            if(datasetName == ''):
                totalRecords = graph.cypher.execute("MATCH (n:User {id:{friendid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN r.atTime ORDER BY r.atTime DESC;", {"friendid": friend['friend.id'], "pid": record['p.id']})
            elif(datasetName == 'FS'):
                totalRecords = graph.cypher.execute("MATCH (n:FSUser {id:{friendid}})-[r:VISITED]->(p:FSPlace {id:{pid}}) RETURN r.atTime ORDER BY r.atTime DESC;", {"friendid": friend['friend.id'], "pid": record['p.id']})
            elif(datasetName ==  'GWL'):
                totalRecords = graph.cypher.execute("MATCH (n:GWLUser {id:{friendid}})-[r:VISITED]->(p:GWLPlace {id:{pid}}) RETURN r.atTime ORDER BY r.atTime DESC;", {"friendid": friend['friend.id'], "pid": record['p.id']})
            elif(datasetName == 'CA'):
                totalRecords = graph.cypher.execute("MATCH (n:CAUser {id:{friendid}})-[r:VISITED]->(p:CAPlace {id:{pid}}) RETURN r.atTime ORDER BY r.atTime DESC;", {"friendid": friend['friend.id'], "pid": record['p.id']})
            # get all visit records by user of p.id
            if(datasetName == ''):
                userVisitRecords = graph.cypher.execute("MATCH (n:User {id:{userid}})-[r:VISITED]->(p:Place {id:{pid}}) RETURN r.atTime;", {"userid": userID, "pid": record['p.id']})
            elif(datasetName == 'FS'):
                userVisitRecords = graph.cypher.execute("MATCH (n:FSUser {id:{userid}})-[r:VISITED]->(p:FSPlace {id:{pid}}) RETURN r.atTime;", {"userid": userID, "pid": record['p.id']})
            elif(datasetName ==  'GWL'):
                userVisitRecords = graph.cypher.execute("MATCH (n:GWLUser {id:{userid}})-[r:VISITED]->(p:GWLPlace {id:{pid}}) RETURN r.atTime;", {"userid": userID, "pid": record['p.id']})
            elif(datasetName == 'CA'):
                userVisitRecords = graph.cypher.execute("MATCH (n:CAUser {id:{userid}})-[r:VISITED]->(p:CAPlace {id:{pid}}) RETURN r.atTime;", {"userid": userID, "pid": record['p.id']})


            # get p.id catgory
            if(datasetName == ''):
                q =  graph.cypher.execute("MATCH (p:Place {id:{pid}}) RETURN p.category",{"pid": record['p.id']})
            elif(datasetName == 'FS'):
                q =  graph.cypher.execute("MATCH (p:FSPlace {id:{pid}}) RETURN p.category",{"pid": record['p.id']})
            elif(datasetName ==  'GWL'):
                q =  graph.cypher.execute("MATCH (p:GWLPlace {id:{pid}}) RETURN p.category",{"pid": record['p.id']})
            elif(datasetName == 'CA'):
                q =  graph.cypher.execute("MATCH (p:CAPlace {id:{pid}}) RETURN p.category",{"pid": record['p.id']})

            if (len(q) > 0):
                cate = q[0]['p.category']
            else:
                cate = 'no category'

            for userVisitRecord in userVisitRecords:
                # get each user visit record time of p.id
                userVisitTime = float(userVisitRecord['r.atTime'])

                for totalR in totalRecords:
                    if(userVisitTime > float(totalR['r.atTime'])):

                        interval = int(float(userVisitTime)) - int(float(totalR['r.atTime']))
                        toDay = interval / 86400

                        if(datasetName == ''):
                            locData = graph.cypher.execute("MATCH (p:Place {id:{pid}}) RETURN p.latitude,p.longitude;", {"pid": record['p.id']})
                        elif(datasetName == 'FS'):
                            locData = graph.cypher.execute("MATCH (p:FSPlace {id:{pid}}) RETURN p.latitude,p.longitude;", {"pid": record['p.id']})
                        elif(datasetName ==  'GWL'):
                            locData = graph.cypher.execute("MATCH (p:GWLPlace {id:{pid}}) RETURN p.latitude,p.longitude;", {"pid": record['p.id']})
                        elif(datasetName == 'CA'):
                            locData = graph.cypher.execute("MATCH (p:CAPlace {id:{pid}}) RETURN p.latitude,p.longitude;", {"pid": record['p.id']})

                        dis=distance_on_unit_sphere(float(mflocation[0]), float(mflocation[1]), float(locData[0]['p.latitude']), float(locData[0]['p.longitude']))

                        pids.append(record['p.id'])
                        distances.append(dis)
                        days.append(toDay)
                        categorys.append(cate)
                        visiteT.append(userVisitTime)

                        #each following relationship record json format:
                        #fid = 123456
                        #pids = [1,2,3,4,5,6,7,8,9]
                        #days = [9,8,7,6,5,4,3,2,1]
                        #diss = [5,5,5,5,5,5,5,5,5]
                        #d = {'fid':fid,'pids':pids,'diss':diss,'days':days}
                        #alld = [], alled.append(d), json.dumps(alld)

                        break
        c = len(pids)
        followData = {'fid':str(fid),'pid':pids,'dis':distances,'day':days,'category':categorys,'visited Time':visiteT,'count':c}
        if(c>0):
            userfollowData.append(followData)


    trainSet = []
    testSet = []

    # print len(userfollowData)

    for usfd in userfollowData:
        fid = usfd['fid']
        pids = usfd['pid']
        dis = usfd['dis']
        days = usfd['day']
        categorys = usfd['category']
        visiteTs = usfd['visited Time']

        pids_train = []
        dis_train = []
        days_train = []
        categorys_train = []
        visiteTs_train = []

        pids_test = []
        dis_test = []
        days_test = []
        categorys_test = []
        visiteTs_test = []

        for i in xrange(len(visiteTs)):
            if(float(visiteTs[i]) < period_marker):
                pids_train.append(pids[i])
                dis_train.append(dis[i])
                days_train.append(days[i])
                categorys_train.append(categorys[i])
                visiteTs_train.append(visiteTs[i])

            elif(float(visiteTs[i]) >= period_marker):
                pids_test.append(pids[i])
                dis_test.append(dis[i])
                days_test.append(days[i])
                categorys_test.append(categorys[i])
                visiteTs_test.append(visiteTs[i])

        fData_train= {'fid':fid,'pid':pids_train,'dis':dis_train,'day':days_train,'category':categorys_train,'visited Time':visiteTs_train,'count':len(pids_train)}
        fData_test= {'fid':fid,'pid':pids_test,'dis':dis_test,'day':days_test,'category':categorys_test,'visited Time':visiteTs_test,'count':len(pids_test)}
        if(len(pids_train) > 0):
            trainSet.append(fData_train)
        if(len(pids_test) > 0):
            testSet.append(fData_test)



    if (datasetName == ''):
        dirName = 'fb'
    else:
        dirName = datasetName

    sorted_followData_all = sorted(userfollowData, key=lambda x: x['count'], reverse=True)
    sorted_followData_train = sorted(trainSet, key=lambda x: x['count'], reverse=True)
    sorted_followData_test = sorted(testSet, key=lambda x: x['count'], reverse=True)

    fDict_train = {}
    fDict_test = {}
    fDict_d = {}

    for i in sorted_followData_train:
        fDict_train[i['fid']] = 1

    for i in sorted_followData_test:
        fDict_test[i['fid']] = 1

    for i in fDict_test:
        if(i in fDict_train):
            fDict_d[i] = 1
    try:
        result = float(len(fDict_d)) / len(fDict_train)
    except:
        result = 0.0
    t = (userID,result)
    results.append(t)

    # rangelimit = int(0.1 * len(sorted_followData))
    # limitlist = []
    # for i in xrange(rangelimit+1):
        # limitlist.append(sorted_followData[i])

    w  = open('/home/ytwen/verify7030/'+dirName+'/'+userID+'_all','w')
    w.write(json.dumps(sorted_followData_all))
    w.close()

    y  = open('/home/ytwen/verify7030/'+dirName+'/'+userID+'_train','w')
    y.write(json.dumps(sorted_followData_train))
    y.close()

    z  = open('/home/ytwen/verify7030/'+dirName+'/'+userID+'_test','w')
    z.write(json.dumps(sorted_followData_test))
    z.close()


print "# Finish calculating following relationship"
print "###########################################"

if (datasetName == ''):
    dirName = 'fb'
else:
    dirName = datasetName
a = open('/home/ytwen/verify7030/'+dirName+'/result.csv','w')
for r in results:
    a.write(str(r[0])+','+str(r[1])+'\n')
a.close()

print "Finish saving result at:"+"/home/ytwen/verify7030/"+dirName+"/result.csv"













