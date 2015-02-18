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
from random import shuffle
from py2neo.packages.httpstream import http
http.socket_timeout = 9999


def getPrecisionAndRecall(trainSet, testSet):
    response = []
    groundtruth = []

    for fid in trainSet:
        # fid = train['fid']
        if fid not in response:
            response.append(fid)
        else:
            continue

    for fid in testSet:
        # fid = test['fid']
        if fid not in groundtruth:
            groundtruth.append(fid)
        else:
            continue

    postive = 0

    # print response, groundtruth

    for fid in response:
        if fid in groundtruth:
            postive = postive + 1
        else:
            continue

    precision = float(postive) / len(response)
    recall = float(postive) / len(groundtruth)

    return precision, recall


def getTopKUser(k, follow):

    # followDic = {follow[i]: followcount[i] for i in xrange(len(follow))}

    sorted_d = sorted(
        follow.items(), key=operator.itemgetter(1), reverse=True)

    topklist = []

    if len(sorted_d) > k:
        for i in xrange(k):
            topklist.append(sorted_d[i][0])  # append key 'id'
    else:
        for i in xrange(len(sorted_d)):
            topklist.append(sorted_d[i][0])

    return topklist


# FB


similarityData = open('/home/ytwen/similarityid_fb_5_15')  # FB
followKData = open('/home/ytwen/msfollowid_fb_5_1')  # FB


sDataList = json.load(similarityData)
fDataList = json.load(followKData)

sDataDic = {}
fDataDic = {}

for s in sDataList:
    uid = s['uid']
    similarids = s['similarID']
    # for i in similarids:
      # print i
    sDataDic[uid] = similarids

for f in fDataList:
    uid = f['uid']
    followids = f['Followed']
    for i in followids:
      print i
    fDataDic[uid] = (followids)


allDic = {}

for u in sDataDic:
    allDic[u] = {'similarID': sDataDic[u], 'followID': fDataDic[
        u]}


w = open('/home/ytwen/exp/PrecisionAndRecall_categorySimiliarity_FB.csv', 'w')

for u in allDic:
    pandrList = []
    for i in xrange(5):
        responseSet = allDic[u]['similarID'][i]
        groundtruthSet = getTopKUser(15, allDic[u]['followID'][i])
        # print responseSet,groundtruthSet
        result = getPrecisionAndRecall(responseSet, groundtruthSet)
        pandrList.append(result)

    s = ''
    for i in pandrList:
        s = s + str(i[0]) + ',' + str(i[1]) + ','
    w.write(str(u) + ',' + s + '\n')

w.close()


# CA


similarityData = open('/home/ytwen/similarityid_CA_5_30')  # FB
followKData = open('/home/ytwen/msfollowid_CA_5_1')  # FB


sDataList = json.load(similarityData)
fDataList = json.load(followKData)

sDataDic = {}
fDataDic = {}

for s in sDataList:
    uid = s['uid']
    similarids = s['similarID']
    sDataDic[uid] = similarids

for f in fDataList:
    uid = f['uid']
    followids = f['Followed']
    fDataDic[uid] = (followids)


allDic = {}

for u in sDataDic:
    allDic[u] = {'similarID': sDataDic[u], 'followID': fDataDic[
        u]}


w = open('/home/ytwen/exp/PrecisionAndRecall_categorySimiliarity_CA.csv', 'w')

for u in allDic:
    pandrList = []
    for i in xrange(5):
        responseSet = allDic[u]['similarID'][i]
        groundtruthSet = getTopKUser(30, allDic[u]['followID'][i])
        result = getPrecisionAndRecall(responseSet, groundtruthSet)
        pandrList.append(result)

    s = ''
    for i in pandrList:
        s = s + str(i[0]) + ',' + str(i[1]) + ','
    w.write(str(u) + ',' + s + '\n')

w.close()
