#!/usr/bin/env python
import sys
import os
import MySQLdb
import MySQLdb.cursors
import time
import warnings
warnings.filterwarnings("ignore")
class GetMysqlStatus(object):
    def __init__(self,port,action,filename):
	self._port=port
	self._action=action
	self._filename=filename
    def getstatus(self):
	conn=MySQLdb.connect(host='localhost',
			     user="zabbix",
			     passwd="a0KChuME4WREISd0f$",
		  	     db="",
                             port=int(self._port),
			     unix_socket='/tmp/mysql%s.sock' % self._port)
        cur=conn.cursor()
        cur.execute('show global status;')
        results=cur.fetchall()
        cur.close()
	return results
    def GetSlave_status(self):
        conn=MySQLdb.connect(host='localhost',
				user="zabbix",
				passwd="a0KChuME4WREISd0f$",
				db="",
				port=int(self._port),
				cursorclass = MySQLdb.cursors.DictCursor,
				unix_socket='/tmp/mysql%s.sock' % self._port)
        cur=conn.cursor()
        cur.execute('show slave status;')
        results=cur.fetchall()
	cur.close()
        if results == ():
            return 'Null'
	else:
	    return results[0]
    def check_file(self):
        if not os.path.exists(self._filename):
	    print 0 
            r=self.getstatus()
            f=open(self._filename,'w')
            for line in r:
                l='%s %s\n' % (line[0],line[1])
                f.write(l)
	    f.close()
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
	       f.close()
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
	f.close()
    def get_mysql_status(self):
	results=self.getstatus()
        for line in results:
	    if line[0] == self._action :
	        print line[1]
    def get_slave_delay(self):
	result = self.GetSlave_status()
	if result == 'Null':
	    print 5
	else:
	    print result['Seconds_Behind_Master']
    def get_slave_running_status(self):
        result = self.GetSlave_status()
        if result == 'Null':
            print 5 
        else:
	    list = ['%s' % result['Slave_IO_Running']  ,'%s' % result['Slave_SQL_Running']]
	    count = list.count('Yes')
	    print count

if __name__ == '__main__' :
    port=sys.argv[1]
    action=sys.argv[2]
    root_path = os.path.dirname(__file__)
    if not os.path.exists('%s/log' % root_path) :    
	os.makedirs('%s/log' % root_path)
    filename='%s/log/old_status.txt_%s_%s' % (root_path,port,action)
    c=GetMysqlStatus(port,action,filename)
    st=['Com_update','Com_select','Com_insert','Com_delete','Com_commit','Com_rollback']
    if action in st:
    	c.get_mysql_qps()
    elif action in ('Threads_connected','Uptime'):
	c.get_mysql_status()	
    elif action == 'Behind_Master':
	c.get_slave_delay()
    elif action == 'Slave_running':
	c.get_slave_running_status()
[root@manager_252 mysql]# 

