from os import listdir
import operator
import matplotlib
matplotlib.use('Agg')
from  matplotlib import pyplot
import json
import re
#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()

#code for drawing the plot goes here

#lt.savefig("output.svg")
#plt.savefig("output.png") 


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


def drawDis(data):
    print data
    dataL=[]
    interval=['<=50','50-100','100-200','200-400','400-800','800-1600','>1600']
    for inter in interval:
        dataL.append(data[inter])
    plt = pyplot
    plt.plot(interval,datal) 
    plt.savefig('/home/ytwen/observationData_follower_one/fb/sumDistance.png')
    plt.close()

#path = '/home/ytwen/observationData_follower_one/fb'
#followDic = {}
#disDic={}
#for followdata in listdir(path):
#    if (followdata == 'sumData.csv') :
#        continue
#    if ('.png' in followdata):
#        continue
#
#    f = open(path+'/'+followdata)
#    
#    for line in f.readlines():
#         m=re.match('(.+)\,(.+)\,(\[.*\])\,(\[.*\])',line)
#         #split = line.split(',')
#         #if( len(split) < 4):
#         #    continue
#         if m is not None:
#             data = json.loads(m.group(3))
#             for dis in data:
#                 key = getdistance(dis)
#                 #print key
#                 if(key in disDic):
#                     disDic[key] = disDic[key] + 1
#                 else:
#                     disDic[key] = 0
    
#drawDis(disDic)

plt = pyplot
a=[1,2,3,5]
b=['abc','bddd','sssc','dff']
plt.plot(a)
plt.xticks(range(len(a)), b, size='small')
plt.savefig('/home/ytwen/test.png')
plt.close()

#        print line.split(',')
#        sum = sum + int(line.split(',')[1])
    
#    followDic[followdata] = int(sum)

#sorted_x = sorted(followDic.items(), key=operator.itemgetter(1),reverse=True)

#topk = int(0.2 * len(sorted_x)) 

#for i in xrange(topk+1):
#    plt = pyplot
#    f = open(path+'/'+sorted_x[i][0])
#    datalist = []
#    count = 0
#    for l in f.readlines():
#        if (count == 100):
#            break
#        datalist.append(l.split(',')[1])
#        count = count + 1

#    plt.plot(datalist)
#    plt.ylabel('follow counts')
#    plt.xlabel('days')
#    plt.savefig(path+'/'+'Num-'+str(i)+'.png')
#    plt.close()

