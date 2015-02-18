from os import listdir
import operator
import matplotlib
matplotlib.use('Agg')
from  matplotlib import pyplot
import json
import re
import math

#math.log10(x) get log10(x) value




def getprob(d):
    s = 0

    if type(d) is list:
        for i in d:
            s = s + i
        for i in xrange(len(d)):
            d[i] = float(d[i])/s

    elif type(d) is dict:
        for i in d:
            s = s + d[i]
        for i in d:
            d[i] = float(d[i])/s

    return d


# def drawTimeSum(t1,t2,t3):
#     plt = pyplot
#     plt.plot(t1,label='FB')
#     plt.plot(t2,label='GWL')
#     plt.plot(t3,label='FS-CA')
#     plt.legend(loc='upper right', shadow=True)
#     plt.ylabel('Probabilty')
#     plt.xlabel('Days')
#     # plt.ylim([0,1])
#     plt.savefig('/home/ytwen/chart/all/timev2.png')
#     plt.close()


def drawTimeSum(t1,t3):
    plt = pyplot
    plt.plot(t1,label='FB')
    # plt.plot(t2,label='GWL')
    plt.plot(t3,label='FS-CA')
    plt.legend(loc='upper right', shadow=True)
    plt.ylabel('Probabilty')
    plt.xlabel('Days')
    # plt.ylim([0,1])
    plt.savefig('/home/ytwen/chart/all/timev2_FB_CA.png')
    plt.close()



def getdistance(dis):
    if(dis <= 1):
        return 1
    elif(dis > 1 and dis <= 10):
        return 10
    elif(dis > 10 and dis <= 100):
        return 100
    elif(dis > 100 and dis <= 1000):
        return 1000
    elif(dis > 1000 and dis <= 10000):
        return 10000
    elif(dis > 10000 ):
        return 100000





# def drawDisSum(d1,d2,d3):
#     plt = pyplot

#     sorted_w = sorted(d1.items(), key=operator.itemgetter(0), reverse=False)
#     x = [i[0] for i in sorted_w]
#     y = [i[1] for i in sorted_w]

#     plt.semilogx(x,y,label='FB')

#     sorted_w = sorted(d2.items(), key=operator.itemgetter(0), reverse=False)
#     x = [i[0] for i in sorted_w]
#     y = [i[1] for i in sorted_w]

#     plt.semilogx(x,y,label='GWL')

#     sorted_w = sorted(d3.items(), key=operator.itemgetter(0), reverse=False)
#     x = [i[0] for i in sorted_w]
#     y = [i[1] for i in sorted_w]

#     plt.semilogx(x,y,label='FS-CA')

#     plt.legend(loc='upper right', shadow=True)

#     plt.ylabel('Probabilty')
#     plt.xlabel('Distance')
#     # plt.ylim([0,1])
#     plt.savefig('/home/ytwen/chart/all/disv2.png')
#     plt.close()


def drawDisSum(d1,d3):
    plt = pyplot

    sorted_w = sorted(d1.items(), key=operator.itemgetter(0), reverse=False)
    x = [i[0] for i in sorted_w]
    y = [i[1] for i in sorted_w]

    plt.semilogx(x,y,label='FB')

    # sorted_w = sorted(d2.items(), key=operator.itemgetter(0), reverse=False)
    # x = [i[0] for i in sorted_w]
    # y = [i[1] for i in sorted_w]

    # plt.semilogx(x,y,label='GWL')

    sorted_w = sorted(d3.items(), key=operator.itemgetter(0), reverse=False)
    x = [i[0] for i in sorted_w]
    y = [i[1] for i in sorted_w]

    plt.semilogx(x,y,label='FS-CA')

    plt.legend(loc='upper right', shadow=True)

    plt.ylabel('Probabilty')
    plt.xlabel('Distance')
    # plt.ylim([0,1])
    plt.savefig('/home/ytwen/chart/all/disv2_FB_CA.png')
    plt.close()


def getDataFromDataset(dataset):
    print "Start getting data from :",dataset
    path = '/home/ytwen/observationData_follower_one/v2/'+dataset
    # followDic = {}
    disDic={}
    sumCount=[]
    # timelist=[]
    # dislist=[]
    for i in range(0,100):
        sumCount.append(0)

    for followdata in listdir(path):
        if (followdata == 'sumData.csv') :
            continue
        if ('.png' in followdata):
            continue
        if ('distance' in followdata):
            continue

        f = open(path+'/'+followdata)
        followCount = 0
        for line in f.readlines():

             m=re.match('(.*)\,(.*)\,(\[.*\])\,(\[.*\])',line)

             if m is not None:

                 if (int(m.group(1)) > 99):
                     break
                 sumCount[int(m.group(1))] = sumCount[int(m.group(1))] + int(m.group(2))
                 # followCount = followCount + int(m.group(2))
                 disdata = json.loads(m.group(3))
                 for dis in disdata:
                     # timelist.append(int(m.group(1)))
                     # dislist.append(int(dis))
                     key = getdistance(dis)
                     if(key in disDic):
                         disDic[key] = disDic[key] + 1
                     else:
                         disDic[key] = 0

        # if(followCount > 0):
            # followDic[followdata] = int(followCount)


    return sumCount,disDic

fb = getDataFromDataset('FB')
gwl = getDataFromDataset('GWL')
CA = getDataFromDataset('CA')

# drawTimeSum(getprob(fb[0]),getprob(gwl[0]),getprob(CA[0]))
# drawDisSum(getprob(fb[1]),getprob(gwl[1]),getprob(CA[1]))

drawTimeSum(getprob(fb[0]),getprob(CA[0]))
drawDisSum(getprob(fb[1]),getprob(CA[1]))
