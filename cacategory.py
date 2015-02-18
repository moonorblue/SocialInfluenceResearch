import json
import re
from py2neo import Graph
from py2neo import Node, Relationship


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
for line in f.readlines():
  m=re.match('(.+)\,(.+)\,(\[.*\])\,(\[.*\])',line)
  for place in json.loads(m.group(4)):
    q = graph.cypher.execute("MATCH (p:CAPlace {id:{id}}) RETURN p.category;",{"id":place})
    for i in q:
      for x in eval(i['p.category']):
        if( len(x) > 0):
          if(x in placeMainCatDic):
            placeMainCatDic[x] = placeMainCatDic[x] + 1
          else:
            placeMainCatDic[x] = 1

sumC = 0

for i in placeMainCatDic:
  print i
  sumC = sumC + int(placeMainCatDic[i])

w=open('/home/ytwen/categoryperctenage_CA.csv','w')

for i in placeMainCatDic:
  w.write(str(i)+','+str(float(float(placeMainCatDic[i])/sumC)*100)+'\n')

w.close()




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
