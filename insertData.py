from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir



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
        graph.cypher.execute("MERGE (user:User {id:{A}}) MERGE (friend:User {id:{B}}) MERGE (user)-[r:KNOWS]->(friend)",{"A":userID,"B":friend})


rootPath = "/home/ytwen/fbdata/"

for user in listdir(rootPath):
    insertUserNode(user)


    

#graph = Graph()

#Save User Node

#Save User FriendShip

#Save Checkin Node

#Save Location Node

#Save User to Checkin / Location Relation with time in relation property
