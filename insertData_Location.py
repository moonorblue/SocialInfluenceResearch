from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time

queryList=[]
class CheckinObj(object):
    objid=""
    name=""
    data=""
    	
#class LocationObj(object):

class PlaceObj(object):
    placeID=""
    name=""
    city=""
    country=""
    latitude=0
    longitude=0

def getFriends(userID):

    rootPath = "/home/ytwen/fbdata/"+userID
    friends = []
    for friend in listdir(rootPath):
        if(friend != userID):
            friends.append(friend)
    
    return friends


def insertUserNode(userID):
    graph = Graph()
    friends = getFriends(userID)
    for friend in friends:
        graph.cypher.execute("MERGE (user:User {id:{A}}) MERGE (friend:User {name:{B}}) MERGE (user)-[r:KNOWS]->(friend)",{"A":userID,"B":friend})


recordC=[]
recordL=[]
def getAllPlaceData(userID):
    rootPath = "/home/ytwen/fbdata/"+userID
    for friend in listdir(rootPath):
        #if(friend in record):
        #    break;
        #else:
        #    record.append(friend)

        furtherPath = rootPath+'/'+friend
        for folder in listdir(furtherPath):
            if(folder == "checkin"):
                if(friend in recordC):
                    break
                else:
                    recordC.append(friend)
                    getPlace(furtherPath+'/'+folder,friend)
            elif(folder == "location"):
                if(friend in recordL):
                    break
                else:
                    recordL.append(friend)
                    getPlace(furtherPath+'/'+folder,friend)
        #     if(friend in record):
        #         break;
        #     else:
        #         record.append(friend)
            #getPlace(furtherPath+'/'+folder,friend)
    #        if(folder == "checkin"):
                       
    #        elif(folder == "location"):
             
            # print friend+" - "+folder  

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
        

#def parseLocation(path,uID): 
def insertPlaceNode(placeID):
    #graph = Graph()
    #statement = "CREATE (place:Place {id:{A}}) "
    #tx = graph.cypher.begin()
    
    graph.cypher.execute("CREATE (place:Place {id:{A}}) ",{"A":placeID})


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


#add_place(j)
#tx.commit()
graph = Graph()
rootPath = "/home/ytwen/fbdata/"
counter=0
for user in listdir(rootPath):
    #insertUserNode(user)
    getAllPlaceData(user)

print counter

#graph = Graph()

#Save User Node

#Save User FriendShip

#Save Checkin Node

#Save Location Node

#Save User to Checkin / Location Relation with time in relation property
