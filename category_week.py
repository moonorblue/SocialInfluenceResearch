import json
import re
from py2neo import Graph
from py2neo import Node, Relationship


f = open('/home/ytwen/pythoncode/fb_list_category.csv')
dic = {}
for line in f.readlines():
  dic[line.split(',')[0].strip('\n')] = line.split(',')[1].strip('\n')

print dic


graph = Graph()

path = '/home/ytwen/observationData_follower_one/fb/sumData.csv'
f = open(path)

placeMainCatDic={}
placeSubCatDic={}
placeMainCatDic['Local business'] = 1
rootPath = "/home/ytwen/placeData/"
catDic={}
for line in f.readlines():
  m=re.match('(.+)\,(.+)\,(\[.*\])\,(\[.*\])',line)
  for place in json.loads(m.group(4)):
    x = open(rootPath+place)
    j = json.load(x)
    category = 0
    category_list = []
    if( 'category' in j):
#      print j['category']
#      print j['category'].encode()
      category = j['category'].encode()
    if( 'category_list' in j ):
      category_list = j['category_list']


    if(category == 'Local business'):

      for cat in category_list:
        if(cat['name'] in dic):
          cate = dic[cat['name']]
          if(len(cate)>1 and cate !="0"):
            graph.cypher.execute("MATCH (n:Place { id: {id} }) SET n.category = {cat} ;",{"id":place,"cat":cate})
            if(cate not in placeMainCatDic):
              placeMainCatDic[cate] = 1
            else:
              placeMainCatDic[cate] = placeMainCatDic[cate] + 1
          else:
              placeMainCatDic['Local business'] = placeMainCatDic['Local business'] + 1
        break

    elif(len(str(category))>1 and category != 0):
      if(category not in placeMainCatDic):
        placeMainCatDic[category] = 1
      else:
        placeMainCatDic[category] = placeMainCatDic[category] + 1


sumC = 0

for i in placeMainCatDic:
  print i
  sumC = sumC + int(placeMainCatDic[i])

w=open('/home/ytwen/categoryperctenage.csv','w')

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
