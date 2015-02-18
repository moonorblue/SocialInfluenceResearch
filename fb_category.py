from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import re



#path = '/home/ytwen/observationData_follower_one/fb/sumData.csv'
#f = open(path,'r')
#placeDic={}
#for line in f.readlines():
#    m=re.match('(.+)\,(.+)\,(\[.*\])\,(\[.*\])',line)
#    
#    for place in json.loads(m.group(4)):
#        if(place in placeDic):
#	    break
#	else:
#	    placeDic[place] = 'Default'

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
#	        placeSubCatDic[cat['name']] = 1

#w = open('/home/ytwen/fb_main_category.csv','w')
#v = open('/home/ytwen/fb_sub_category.csv','w')

#for main in placeMainCatDic:
#    w.write(str(main)+'\n')

#w.close()

#for sub in placeSubCatDic:
#    v.write(str(sub)+'\n')


#v.close()

path = '/home/ytwen/observationData_follower_one_interest/'
dic={}
for user in listdir(path):
    f = open(path+user)
    for line in f.readlines():
        cat = line.split(',')[0]
	if(cat not in dic):
            dic[cat]=1

w = open('/home/ytwen/fb_main_category_2.csv','w')
for x in dic:
    w.write(str(x)+'\n')
w.close()

