from py2neo import Graph
import sys
import json
from random import shuffle
from copy import deepcopy
import math

g = Graph()


# def cosine_similarity(v1,v2):
#     sumxx, sumxy, sumyy = 0, 0, 0
#     for i in range(len(v1)):
#         x = v1[i]; y = v2[i]
#         sumxx += x*x
#         sumyy += y*y
#         sumxy += x*y
#     return sumxy/math.sqrt(sumxx*sumyy)



##fb
w = open('/home/ytwen/category_fb')
z = open('/home/ytwen/userfeatureList_fb_7030_5','w')


allCategory = json.load(w)
allusers = g.cypher.execute("MATCH (n:User) RETURN n.id;")

userfeatureList = []
for user in allusers:
  userid = str(user['n.id'])
  checkins = g.cypher.execute("MATCH (n:User {id:{uid}})-[r:VISITED]->(p:Place) RETURN p.category,r.id,p.id,r.atTime;",{"uid":userid})
  marker = 0.7*len(checkins)
  checkinList = [ (i['p.category'],i['r.id'],i['r.atTime'],i['p.id']) for i in checkins]

  f7=[]
  c3=[]

  for i in xrange(5):
    copy = deepcopy(checkinList)
    shuffle(copy)
    checkin70 = []
    for j in xrange(int(marker)):
      checkin70.append(copy.pop())
    checkin30 = copy

    feature70 = [0 for i in allCategory]
    cid30 = []

    for checkin in checkin70:
      category = str(checkin[0])
      categoryIndex = allCategory.index(category)
      feature70[categoryIndex] += 1

    for checkin in checkin30:
      checkinid = str(checkin[1])
      time = str(checkin[2])
      pid = str(checkin[3])
      cid30.append((checkinid,time,pid))

    f7.append(feature70)
    c3.append(cid30)


  userfeatureList.append({"uid":userid,"70_feature":f7,"30_checkinid":c3})
  # print "uid:",userid,'  feature',featuteList

z.write(json.dumps(userfeatureList))
z.close()

##CA
w = open('/home/ytwen/category_CA')
z = open('/home/ytwen/userfeatureList_CA_7030_5','w')


allCategory = json.load(w)
allusers = g.cypher.execute("MATCH (n:CAUser) RETURN n.id;")

userfeatureList = []
for user in allusers:

  userid = str(user['n.id'])
  checkins = g.cypher.execute("MATCH (n:CAUser {id:{uid}})-[r:VISITED]->(p:CAPlace) RETURN p.category,r.id,p.id,r.atTime;",{"uid":userid})
  marker = 0.7*len(checkins)
  checkinList = [ (i['p.category'],i['r.id'],i['r.atTime'],i['p.id']) for i in checkins]

  f7=[]
  c3=[]

  for i in xrange(5):
    copy = deepcopy(checkinList)
    shuffle(copy)
    checkin70 = []
    for j in xrange(int(marker)):
      checkin70.append(copy.pop())
    checkin30 = copy

    feature70 = [0 for i in allCategory]
    cid30 = []

    for checkin in checkin70:
     category = eval(str(checkin[0]))
     weight = len(category) - 1

     for c in category:
      if len(c) > 0 :
        categoryIndex = allCategory.index(c)
        feature70[categoryIndex] += float(1)/weight


    for checkin in checkin30:
      checkinid = str(checkin[1])
      time = str(checkin[2])
      pid = str(checkin[3])
      cid30.append((checkinid,time,pid))


    f7.append(feature70)
    c3.append(cid30)


  userfeatureList.append({"uid":userid,"70_feature":f7,"30_checkinid":c3})
  # print "uid:",userid,'  feature',featuteList

z.write(json.dumps(userfeatureList))
z.close()