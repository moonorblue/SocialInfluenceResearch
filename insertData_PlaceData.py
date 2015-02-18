from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time

queryList=[]

def insertUserNode(userID):
    graph = Graph()
    friends = getFriends(userID)
    for friend in friends:
        graph.cypher.execute("MERGE (user:User {id:{A}}) MERGE (friend:User {name:{B}}) MERGE (user)-[r:KNOWS]->(friend)",{"A":userID,"B":friend})

             

def getPlace(path,uID):
    jsonFile = path+'/'+uID
    json_data=open(jsonFile)
    data = json.load(json_data)
    #print "Folder: "+jsonFile
    global counter
    for eachData in data:
        if('place' in eachData):
            itemID = eachData['id']
            placeID = eachData['place']['id']
            timestamp = time.mktime(time.strptime(eachData['created_time'], '%Y-%m-%dT%H:%M:%S+0000'))
            #print ("UserID: "+uID+"  PlaceID: "+str(placeID)+"   time: "+str(timestamp))
            insertVisit(uID,itemID,placeID,timestamp)            
            counter= counter + 1
            #print counter
            #print "In "+jsonFile 

def insertVisit(uID,itemID,placeID,timestamp):
    graph.cypher.execute("MATCH (n:User {id:{uID}}),(p:Place {id:{pID}}) CREATE UNIQUE (n)-[:VISITED { id:{iid},atTime:{tstamp }}]->(p)",{"uID":uID,"pID":placeID,"iid":itemID,"tstamp":str(timestamp)})
    #graph.cypher.execute("MATCH (n:User {id:{uID}})-[r]->(p:Place {id:{pID}}) DELETE r",{"uID":uID,"pID":placeID})
    #counter = counter + 1

def parseCheckin(path,uID):
    jsonFile = path+'/'+uID
    json_data=open(jsonFile)
    data = json.load(json_data)
    
    for eachData in data:
        #placeobj = PlaceObj()
        #place.placeID = eachData['place']['id']
        #place.name = eachData['place']['name']
        #place.city = eachData['place']['location']['city']
        insertPlaceNode(eachData['place']['id'])

#f=open("/home/ytwen/newJSON",'r')
#j=json.load(f)
#graph = Graph()
#for place in j:
#    insertPlaceNode(place)
#d=json.dumps(j)
#graph = Graph()
#statement = "CREATE (place:Place {id:{A}}) "
#tx = graph.cypher.begin()

def add_place(places):
    for place in places:
        tx.append(statement, {"A":place})
    tx.process()


graph = Graph()
rootPath = "/home/ytwen/placeData/"
counter=0
for place in listdir(rootPath):
    f = open(rootPath+'/'+place)
    j = json.load(f)
    category = 'NONE'
    checkins = 'NONE'
    likes = 'NONE'
    can_post = 'NONE'
    is_community_page = 'NONE'
    is_published = 'NONE'
    location = 'NONE'
    city = 'NONE'
    country = 'NONE'
    latitude = 'NONE'
    longitude = 'NONE'
    lzip = 'NONE'
    name = 'NONE'
    talking_about_count = 'NONE'


    #category
    if( 'category' in j ):
        category  = j['category'].encode()
    #checkins
    if( 'checkins' in j ):
        checkins = j['checkins']
    #likes
    if( 'likes' in j):
        likes = j['likes']
    #can_post
    if( 'can_post' in j):
        can_post = j['can_post']
    #is_community_page
    if( 'is_community_page' in j):
        is_community_page = j['is_community_page']
    #is_published
    if( 'is_published' in j):
        is_published = j['is_published']
    #location
    if( 'location' in j):
        location = j['location']
        #country
        if( 'country' in location):
            country = location['country']
        #city
        if( 'city' in location):
            city = location['city']
        #latitude
        if( 'latitude' in location):
            latitude = location['latitude']
        #longitude
        if( 'longitude' in location):
            longitude = location['longitude']
        #zip
        if( 'zip' in location):
            lzip = location['zip']        
    #name
    if( 'name' in j):
        name = j['name']
    #talking_about_count
    if( 'talking_about_count' in j):
        talking_about_count = j['talking_about_count']
    
    
    graph.cypher.execute("MATCH (p:Place {id:{uid}}) SET p.category = {category} SET p.checkins = {checkins} SET p.likes = {likes} SET p.can_post = {can_post} SET p.is_community_page = {is_community_page} SET p.is_published = {is_published} SET p.city = {city} SET p.country = {country} SET p.latitude = {latitude} SET p.longitude = {longitude} SET p.lzip = {lzip} SET p.name = {name} SET p.talking_about_count = {talking_about_count} ",{"uid":place,"category":category,"checkins":checkins,"likes":likes,"can_post":can_post,"is_community_page":is_community_page,"is_published":is_published,"city":city,"country":country,"latitude":latitude,"longitude":longitude,"lzip":lzip,"name":name,"talking_about_count":talking_about_count})


#graph = Graph()

#Save User Node

#Save User FriendShip

#Save Checkin Node

#Save Location Node

#Save User to Checkin / Location Relation with time in relation property
