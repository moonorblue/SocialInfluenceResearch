from py2neo import Graph
import sys
import json
from random import shuffle
from copy import deepcopy
import math
import operator
from os import listdir
import time
import re
# get top 10%


def getTop10User(dataset):

    dirName = dataset

    path = '/home/ytwen/observationData_follower_one/v2/' + dirName
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
    # rangelimit = 10

    newlist = []
    for i in xrange(rangelimit + 1):
        newlist.append(sorted_x[i][0])

    return newlist


def cosine_similarity(v1, v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    if sumxx * sumyy == 0:
        return 0
    return sumxy / math.sqrt(sumxx * sumyy)


def getVectorFromNum(l, num):
    d = {}
    for userdata in l:
        userid = userdata['uid']
        usercategoryfeature = userdata['70_feature'][num]
        d[userid] = usercategoryfeature

    return d


top10user = getTop10User("FB")
#top10user = ['1297994384']

w = open('/home/ytwen/userfeatureList_fb_7030_5')
r = json.load(w)
z = open('/home/ytwen/similarityid_fb_5_15', 'w')
similar_L = []

for user in top10user:
    uid = user.strip('.csv')
    topsimilar = []
    score = []

    for i in xrange(5):
        dataDic = getVectorFromNum(r, i)
        userVector = dataDic[uid]
        similarityDic = {}
        for data in dataDic:
            if data == uid:
                continue
            similarityDic[data] = cosine_similarity(userVector, dataDic[data])

        sorted_dic = sorted(
            similarityDic.items(), key=operator.itemgetter(1), reverse=True)
        similarList = []
        sList = []
        k = 15
        for i in xrange(k):
            similarList.append(sorted_dic[i][0])
            sList.append(sorted_dic[i][1])
        topsimilar.append(similarList)
        score.append(sList)

    similar_L.append({"uid": uid, "similarID": topsimilar, "score": score})

z.write(json.dumps(similar_L))
z.close()


top10user = getTop10User("CA")

w = open('/home/ytwen/userfeatureList_CA_7030_5')
r = json.load(w)
z = open('/home/ytwen/similarityid_CA_5_30', 'w')
similar_L = []

for user in top10user:
    uid = user.strip('.csv')
    topsimilar = []
    score = []

    for i in xrange(5):
        dataDic = getVectorFromNum(r, i)
        userVector = dataDic[uid]
        similarityDic = {}
        for data in dataDic:
            if data == uid:
                continue
            similarityDic[data] = cosine_similarity(userVector, dataDic[data])

        sorted_dic = sorted(
            similarityDic.items(), key=operator.itemgetter(1), reverse=True)
        similarList = []
        sList = []
        k = 30
        for i in xrange(k):
            similarList.append(sorted_dic[i][0])
            sList.append(sorted_dic[i][1])
        topsimilar.append(similarList)
        score.append(sList)

    similar_L.append({"uid": uid, "similarID": topsimilar, "score": score})

z.write(json.dumps(similar_L))
z.close()
