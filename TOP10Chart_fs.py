from os import listdir
import operator
import matplotlib
matplotlib.use('Agg')
from  matplotlib import pyplot
import json
import re



def drawTimeSum(timelist):
    plt = pyplot   
    plt.plot(timelist)
    plt.ylabel('follow counts')
    plt.xlabel('days')
    plt.savefig('/home/ytwen/chart/timefactor/fs/Top10%-sum.png')
    plt.close()


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


def drawDisSum(data):
    print data
    dataL=[]
    interval=['<=50','50-100','100-200','200-400','400-800','800-1600','>1600']
    for inter in interval:
        if(inter in data): 
            dataL.append(data[inter])
        else:
            dataL.append(0)
    plt = pyplot
    plt.plot(dataL) 
    plt.xticks(range(len(dataL)), interval, size='small')
    #plt.savefig('/home/ytwen/observationData_follower_one/gwl/sumDistance.png')
    plt.savefig('/home/ytwen/chart/distancefactor/fs/Top10%-sum.png')
    #/home/ytwen/chart/timefactor/fb
    plt.close()


def drawTD(timelist,dislist):
    plt = pyplot
    plt.plot(dislist,timelist, 'ro')
    plt.ylabel('days')
    plt.xlabel('distance')
    plt.savefig('/home/ytwen/chart/timedistance/fs/Top10%-sum.png')
    plt.close()
 

def drawTimeTopK(timelist,k):
    plt = pyplot
    plt.plot(timelist)
    plt.ylabel('follow counts')
    plt.xlabel('days')
    plt.savefig('/home/ytwen/chart/timefactor/fs/Top10%-NUM-'+str(k)+'.png')
    plt.close()
 
def drawDisTopK(disDic,k):
    dataL=[]
    interval=['<=50','50-100','100-200','200-400','400-800','800-1600','>1600']
    for inter in interval:
        if(inter in disDic):
            dataL.append(disDic[inter])
        else:
            dataL.append(0)
    plt = pyplot
    plt.plot(dataL)
    plt.xticks(range(len(dataL)), interval, size='small')
    plt.savefig('/home/ytwen/chart/distancefactor/fs/Top10%-NUM-'+str(k)+'.png')
    plt.close() 

def drawTDTopK(timelist,dislist,k):
    plt = pyplot
    plt.plot(dislist,timelist, 'ro')
    plt.ylabel('days')
    plt.xlabel('distance')
    plt.savefig('/home/ytwen/chart/timedistance/fs/Top10%-NUM-'+str(k)+'.png')
    plt.close()

def drawTDWithC(timelist,dislist,c):
    
    dl=[]
    tl=[]
    for x in xrange(len(dislist)):
        if( dislist[x] < int(c)):
            dl.append(dislist[x])
            tl.append(timelist[x])
                
    plt = pyplot
    plt.plot(dl,tl, 'ro')
    plt.ylabel('days')
    plt.xlabel('distance')
    plt.savefig('/home/ytwen/chart/timedistance/fs/Top10%-sumC.png')
    plt.close()

path = '/home/ytwen/observationData_follower_one/fs'
followDic = {}
disDic={}
sumCount=[]
timelist=[]
dislist=[]

for i in range(0,100):
    sumCount.append(0)

for followdata in listdir(path):
    if (followdata == 'sumData.csv') :
        continue
    if ('.png' in followdata):
        continue
    if ('distance' in followdata):
        continue
    #print followdata
    f = open(path+'/'+followdata)
    followCount = 0
    for line in f.readlines():
         #print line
         m=re.match('(.*)\,(.*)\,(\[.*\])\,(\[.*\])',line)
         #split = line.split(',')
         #if( len(split) < 4):
         #    continue
         if m is not None:
             #print m.group(0)
             if (int(m.group(1)) > 99):
                 break
            
             sumCount[int(m.group(1))] = sumCount[int(m.group(1))] + int(m.group(2))

             followCount = followCount + int(m.group(2))

             disdata = json.loads(m.group(3))
             for dis in disdata:
                 timelist.append(int(m.group(1)))
                 dislist.append(int(dis))

                 key = getdistance(dis)
                 #print key
                 if(key in disDic):
                     disDic[key] = disDic[key] + 1
                 else:
                     disDic[key] = 0

    if(followCount > 0):
        followDic[followdata] = int(followCount)

#drawTimeSum(sumCount)    
#drawDisSum(disDic)
#drawTD(timelist,dislist)
#drawTDWithC(timelist,dislist,500)

sorted_x = sorted(followDic.items(), key=operator.itemgetter(1),reverse=True)

rangelimit = int(0.1*len(sorted_x))

followDic = {}
disDicAll={}
sumCount=[]
timelist=[]
dislist=[]

for i in range(0,100):
    sumCount.append(0)

for i in xrange(rangelimit):
    filename = sorted_x[i][0]
    f = open(path+'/'+filename)
    countL=[]
    disDic={}
    tlist=[]
    dlist=[]
    for line in f.readlines():
        m=re.match('(.+)\,(.+)\,(\[.*\])\,(\[.*\])',line)
        if m is not None:

            if (int(m.group(1)) > 99):
	        break
	    sumCount[int(m.group(1))] = sumCount[int(m.group(1))] + int(m.group(2))
	    countL.append(int(m.group(2)))

            disdata = json.loads(m.group(3))
            for dis in disdata:
                tlist.append(int(m.group(1)))
                dlist.append(int(dis))
		timelist.append(int(m.group(1)))
		dislist.append(int(dis))

                key = getdistance(dis)
                    #print key
                if(key in disDic): 
                    disDic[key] = disDic[key] + 1
                else:
                    disDic[key] = 0
		if(key in disDicAll):
		    disDicAll[key] = disDicAll[key] + 1
		else:
		    disDicAll[key] = 0

    drawTimeTopK(countL,i)
    drawDisTopK(disDic,i)
    drawTDTopK(tlist,dlist,i)


drawTimeSum(sumCount)    
drawDisSum(disDicAll)
drawTD(timelist,dislist)
drawTDWithC(timelist,dislist,10000)

#for num in allnum:
#    for i in range(num,num+10):
#        filename = sorted_x[i][0]
#        f = open(path+'/'+filename)
#        countL=[]
#        disDic={}
#        tlist=[]
#        dlist=[]
#        for line in f.readlines():
#            m=re.match('(.+)\,(.+)\,(\[.*\])\,(\[.*\])',line)
#            if m is not None:

#               if (int(m.group(1)) > 99):
#                    break
#                countL.append(int(m.group(2)))

#                disdata = json.loads(m.group(3))
#                for dis in disdata:
#                    tlist.append(int(m.group(1)))
#                    dlist.append(int(dis))

#                    key = getdistance(dis)
                    #print key
#                    if(key in disDic):
#                        disDic[key] = disDic[key] + 1
#                    else:
#                        disDic[key] = 0

#        drawTimeTopK(countL,i)
#        drawDisTopK(disDic,i) 
#        drawTDTopK(tlist,dlist,i)
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

