from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json

allPlace = []
class PlaceObj(object):
    placeID=""
    name=""
    city=""
    country=""
    latitude=0
    longitude=0



def getAllPlaceData(userID):
    rootPath = "/home/ytwen/fbdata/"+userID
    for friend in listdir(rootPath):
        furtherPath = rootPath+'/'+friend
        for folder in listdir(furtherPath):
             getPlace(furtherPath+'/'+folder,friend)
    #        if(folder == "checkin"):
                       
    #        elif(folder == "location"):
               

def getPlace(path,uID):
    jsonFile = path+'/'+uID
    json_data=open(jsonFile)
    data = json.load(json_data)
    
    for eachData in data:
        if('place' in eachData):
            #insertPlaceNode(eachData['place']['id'])
            allPlace.append(eachData['place']['id'])
 

def parseCheckin(path,uID):
    jsonFile = path+'/'+uID
    json_data=open(jsonFile)
    data = json.load(json_data)
    
#    for eachData in data:

        #placeobj = PlaceObj()
        #place.placeID = eachData['place']['id']
        #place.name = eachData['place']['name']
        #place.city = eachData['place']['location']['city']
        #insertPlaceNode(eachData['place']['id'])
        

#def parseLocation(path,uID): 
def insertPlaceNode(placeID):
    graph = Graph()
    graph.cypher.execute("MERGE (place:Place {id:{A}}) ",{"A":placeID})

rootPath = "/home/ytwen/fbdata/"

for user in listdir(rootPath):
    #insertUserNode(user)
    getAllPlaceData(user)

f = open('placeJSON', 'w')    
jsonFile = json.dumps(allPlace)
f.write(jsonFile)
f.close()

#graph = Graph()

#Save User Node

#Save User FriendShip

#Save Checkin Node

#Save Location Node

#Save User to Checkin / Location Relation with time in relation property
