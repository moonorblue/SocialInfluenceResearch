import re
f=open("/home/ytwen/rawdata/fs/socialgraph.dat")
w=open("/home/ytwen/socialgraph.csv",'w')
count = 0
for l in f.readlines():
    print count
	if( count > 1):
		l = l.translate(None, "|")	
		l = l.split()
		uid = l[0]
		fid = l[1]
		w.write(str(uid)+','+str(fid)+'\n')
	if( len(l) > 2 ):
        continue

	count = count + 1
w.close()
