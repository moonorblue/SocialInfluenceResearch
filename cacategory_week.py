import json
import re
from py2neo import Graph
from py2neo import Node, Relationship
import operator


def getdistance(dis):
    if(dis <= 50):
        return '<=50'
    elif(dis > 50 and dis <=100):
        return '50-100'
    elif(dis > 100 and dis <=200):
        return '100-200'
    elif(dis >200 and dis <=400):
        return '200-400'
    elif(dis >400 and dis <=800):
        return '400-800'
    elif(dis >800 and dis <=1600):
        return '800-1600'
    elif(dis >1600):
        return '>1600'


def saveDis(intertype,num,dic):
  path = '/home/ytwen/CAcategory/'+str(intertype)+'/'+str(num)+'.csv'
  w = open(path,'w')

  sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
  #sorted dic
  for t in sorted_x:
    w.write(str(t[0])+','+str(t[1])+'\n')
  w.close()


def getCalDict(dic):
  sumC = 0
  for d in dic:
    sumC = sumC + int(dic[d])

  dic_n={}
  for d in dic:
    dic_n[d] = float(float(dic[d])/sumC)*100

  return dic_n


# f = open('/home/ytwen/pythoncode/fb_list_category.csv')
# dic = {}
# for line in f.readlines():
#   dic[line.split(',')[0].strip('\n')] = line.split(',')[1].strip('\n')

# print dic


graph = Graph()

path = '/home/ytwen/observationData_follower_one/CA/sumData.csv'
f = open(path)

placeMainCatDic={}

catDic={}
weekDic={}
for line in f.readlines():
  m=re.match('(.+)\,(.+)\,(\[.*\])\,(\[.*\])',line)
  pList = json.loads(m.group(4))
  dList = json.loads(m.group(3))
  for i in xrange(len(dList)) :

    recordDic = ''
    # nkey = getdistance(int(dList[i]))
    nkey = int(m.group(1))/7
    if(nkey in weekDic):
      recordDic = weekDic[nkey]
    else:
      recordDic = {}

    pid = pList[i]
    q = graph.cypher.execute("MATCH (p:CAPlace {id:{id}}) RETURN p.category;",{"id":pid})
    for i in q:
      for x in eval(i['p.category']):
        if( len(x) > 0):
          if(x not in recordDic):
            recordDic[x] = 1
          else:
            recordDic[x] = recordDic[x] + 1

    weekDic[nkey] = recordDic


for week in weekDic:
  new_dic = getCalDict(weekDic[week])
  saveDis('Week',str(week),new_dic)


#   for place in json.loads(m.group(4)):
#     q = graph.cypher.execute("MATCH (p:CAPlace {id:{id}}) RETURN p.category;",{"id":place})
#     for i in q:
#       for x in eval(i['p.category']):
#         if( len(x) > 0):
#           if(x in placeMainCatDic):
#             placeMainCatDic[x] = placeMainCatDic[x] + 1
#           else:
#             placeMainCatDic[x] = 1

# sumC = 0

# for i in placeMainCatDic:
#   print i
#   sumC = sumC + int(placeMainCatDic[i])

# w=open('/home/ytwen/categoryperctenage_CA.csv','w')

# for i in placeMainCatDic:
#   w.write(str(i)+','+str(float(float(placeMainCatDic[i])/sumC)*100)+'\n')

# w.close()




#rootPath = "/home/ytwen/placeData/"

#placeMainCatDic={}
#placeSubCatDic={}

#for place in placeDic:
#    f = open(rootPath+place)
#    j = json.load(f)
#    category = 0
#    category_list = []

#    if( 'category' in j):
#        category = j['category'].encode()
#    if( 'category_list' in j ):
#        category_list = j['category_list']

#    if(category not in placeMainCatDic):
#        placeMainCatDic[category]=1
#    if(category == 'Local business'):
#        for cat in category_list:
#            if(cat['name'] not in placeSubCatDic):
#         placeSubCatDic[cat['name']] = 1

#w = open('/home/ytwen/fb_main_category.csv','w')
#v = open('/home/ytwen/fb_sub_category.csv','w')

#for main in placeMainCatDic:
#    w.write(str(main)+'\n')

#w.close()

#for sub in placeSubCatDic:
#    v.write(str(sub)+'\n')
