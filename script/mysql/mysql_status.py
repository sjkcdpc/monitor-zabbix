#!/usr/bin/env python
import sys
import os
import MySQLdb
import time
class GetMysqlStatus(object):
    def __init__(self,port,action,filename):
	self._port=port
	self._action=action
	self._filename=filename
    def getstatus(self):
        conn=MySQLdb.connect(host='localhost',user="root",passwd="",db="mysql",port=int(self._port))
        cur=conn.cursor()
        cur.execute('show global status;')
        results=cur.fetchall()
	return results
    def check_file(self):
        if not os.path.exists(self._filename):
	    print 0 
            r=self.getstatus()
            f=open(self._filename,'w')
            for line in r:
                l='%s %s\n' % (line[0],line[1])
                f.write(l)
            sys.exit()

        elif os.path.exists(self._filename):
           nowtime_seconds=time.time() 
           file_mtime=os.stat(self._filename).st_mtime
           meta_time=int(nowtime_seconds - file_mtime)
           if meta_time > 30 :
               print 0
               r=self.getstatus()
               f=open(self._filename,'w')
               for line in r:
                   l='%s %s\n' % (line[0],line[1])
                   f.write(l)
               sys.exit()

    def get_mysql_qps(self):
        self.check_file()
        results=self.getstatus()
        for line in results:
    	    if line[0] == self._action:
                new=line[1]
        f=open(self._filename,'r')
        for line in f.readlines():
            line=line.split()
            if line[0]==self._action:
    	        old=line[1]
        meta=int(new)-int(old)
        print meta
        f=open(self._filename,'w')
        for line in results:
            l='%s %s\n' % (line[0],line[1])
            f.write(l)
    
if __name__ == '__main__' :
    port=sys.argv[1]
    action=sys.argv[2]
    filename='/etc/zabbix/script/log/old_status.txt_%s_%s' % (port,action)
    c=GetMysqlStatus(port,action,filename)
    c.get_mysql_qps()
