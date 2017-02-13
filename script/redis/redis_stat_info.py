#!/usr/bin/env python
import os
import redis
import sys
import time

class GetRedisStat(object):
    def __init__(self,host,port,filepath,key):
        self._host = host
	self._port = port
	self._key = key
	self._filepath = filepath

    def statredis(self):
	r = redis.Redis(self._host,self._port)	
	statinfo = r.info()
	return statinfo

    def ispathexist(self):
	if not os.path.exists(self._filepath):
	   return 0
	else:
	   return 1

    def Writefile(self,filename):
	info = self.statredis()	
        rwfile = open(filename,'w')
        for k,v in info.iteritems():
            rwfile.write('%s \t %s\n' % (k,v))

    def Operatefile(self,action):
	v = self.ispathexist()
	if v == 0 :
	    self.Writefile(self._filepath)
	    print 0
            sys.exit(0)
	elif v == 1 :
	    if action == 'write':
	        self.Writefile(self._filepath) 
	    
     	    elif action == 'read':
	        rwfile = open(self._filepath,'r')
	        results = dict() 
  	        for line in rwfile.readlines():
	            line = line.split()
	            results[line[0]] = line[1] 
	        return results

    def main(self):	
	info = self.statredis()
	if self._key != 'qps':
	    return info['%s' % self._key]
	elif self._key == 'qps':
	    result = self.Operatefile('read')
	    nowtime = time.time()
            filetime = os.stat(self._filepath).st_mtime
	    meta = nowtime - filetime 
	    if meta  > 30 :
		self.Writefile(self._filepath)
	        return 0
            else:
	        old = result['total_commands_processed']
		new = self.statredis()['total_commands_processed']
		self.Operatefile('write')
		return int(new) - int(old)
if __name__ == '__main__':
    host = sys.argv[1]
    port = sys.argv[2]
    key = sys.argv[3]
    root_path = os.path.dirname(__file__)
    filepath = '%s/log/%s_log.txt' % (root_path,port)
    R =  GetRedisStat(host,port,filepath,key)
    s = R.main()
    print s
