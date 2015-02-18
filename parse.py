import json

f=open("/home/ytwen/placeJSON",'r')
d=json.load(f)

k=[]

for x in d:
   #print x
   if((x in k) == False):
      k.append(x)

x=json.dumps(k)

ff=open("/home/ytwen/newJSON",'w')
ff.write(x)
ff.close()
