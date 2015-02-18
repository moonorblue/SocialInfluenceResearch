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


def getCheckinFromNum(l, num):
	d = {}
	for userdata in l:
		userid = userdata['uid']
		usercheckin = userdata['30_checkinid'][num]
		d[userid] = usercheckin

	return d


def getUserCheckinWithPid(pid, data):
	pList = []
	for d in data:
		if d[2] == pid:
			pList.append(d[1])
	pList.sort()
	return pList


def getUserCheckinWithPidDesc(pid, data):
	pList = []
	for d in data:
		if d[2] == pid:
			pList.append(d[1])
	pList.sort(reverse=True)
	return pList


def getDistincePid(data):
	pList = []
	for d in data:
		if d[2] not in pList:
			pList.append(d[2])
	return pList



countLimit = int(sys.argv[1])

top10user = getTop10User("FB")
# top10user = ['1297994384']

w = open('/home/ytwen/userfeatureList_fb_7030_5')
r = json.load(w)


z = open('/home/ytwen/msfollowid_fb_5_'+str(countLimit), 'w')
MFollow_L = []
tAvg = 0.0
print "START : FB"
for user in top10user:
	uid = user.strip('.csv')
	MFollow = []
	fCount = []
	sumC = 0
	for i in xrange(5):
		dataDic = getCheckinFromNum(r, i)
		uuserRecords = dataDic[uid]
		followDic = {}
		for data in dataDic:
			if data == uid:
				continue
			otherRecords = dataDic[data]
			pids = getDistincePid(otherRecords)

			for p in pids:

				userRecords = getUserCheckinWithPid(p, uuserRecords)
				totalRecords = getUserCheckinWithPidDesc(p, otherRecords)
				# print userRecords,totalRecords

				flag = False
				if len(userRecords) > 0 and len(totalRecords) > 0 :
					for userR in userRecords:
						for totalR in totalRecords:
							if float(userR) > float(totalR):
								if data not in followDic:
									followDic[data] = 1
								else:
									followDic[data] += 1
								flag = True
								break

						if flag == True:
							break
		newDic = {}
		for u in followDic:
			if int(followDic[u]) >= countLimit:
				newDic[u] = followDic[u]


		followUsers = len(newDic)
		fCount.append(followUsers)
		sumC += followUsers

		MFollow.append(newDic)
	totalAvg = sumC / 5
	tAvg +=totalAvg
	MFollow_L.append({'uid':uid,'Followed':MFollow,'FollowCount':fCount,'AvgFollowCount':totalAvg})

print "FB:",str(tAvg/len(top10user))
z.write(json.dumps(MFollow_L))
z.close()


    
top10user = getTop10User("CA")

print "START : CA"
w = open('/home/ytwen/userfeatureList_CA_7030_5')
r = json.load(w)


z = open('/home/ytwen/msfollowid_CA_5_'+str(countLimit),'w')
MFollow_L = []

tAvg = 0.0
for user in top10user:
	uid = user.strip('.csv')
	MFollow = []
	fCount = []
	sumC = 0
	for i in xrange(5):
		dataDic = getCheckinFromNum(r, i)
		uuserRecords = dataDic[uid]
		followDic = {}
		for data in dataDic:
			if data == uid:
				continue
			otherRecords = dataDic[data]
			pids = getDistincePid(otherRecords)

			for p in pids:
				userRecords = getUserCheckinWithPid(p, uuserRecords)
				totalRecords = getUserCheckinWithPidDesc(p, otherRecords)
				# print userRecords,totalRecords
				flag = False
				if len(userRecords) > 0 and len(totalRecords) > 0 :
					for userR in userRecords:
						for totalR in totalRecords:
							# print userR,totalR
							if float(userR) > float(totalR):
								if data not in followDic:
									followDic[data] = 1
								else:
									followDic[data] += 1
								flag = True
								break

						if flag == True:
							break
		newDic = {}
		for u in followDic:
			if int(followDic[u]) >= countLimit:
				newDic[u] = followDic[u]

		followUsers = len(newDic)
		fCount.append(followUsers)
		sumC += followUsers
		
		MFollow.append(newDic)
	totalAvg = sumC / 5
	tAvg +=totalAvg
	MFollow_L.append({'uid':uid,'Followed':MFollow,'FollowCount':fCount,'AvgFollowCount':totalAvg})


print "CA:",str(tAvg/len(top10user))
z.write(json.dumps(MFollow_L))
z.close()



