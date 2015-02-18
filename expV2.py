from py2neo import Graph
from py2neo import Node, Relationship
import os
import itertools
from os import listdir
import json
import time
import cPickle as pickle
from copy import deepcopy
import sys
import re
import operator
import math
from py2neo.packages.httpstream import http
http.socket_timeout = 9999



#全部checkins分成30_70 ,從top 10 user裡面，算每個user follow別人（不一定是朋友，只要是在這個地點上）