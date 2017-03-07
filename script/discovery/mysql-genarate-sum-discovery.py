#!/usr/bin/env python
import os
import json
import hashlib

root_path = os.path.dirname(__file__)
filename='%s/mysqllist.txt' % (root_path)
file = open(filename,'r')
result = {}
newresult = []
for line in file.readlines():
    line = line.split()
    name = line[0]
    ip = line[1]
    type = line[2]
    port = line[3]
    if type == 's' :
        type = 'slaves'
    elif type == 'm':
	type = 'masters'
    key = '%s-%s-%s' % (name,type,port)
    keys = result.keys()
    if key not in keys:
        result['%s' % key] = ip
    elif key in keys:
        value = result['%s' % key]
        result['%s' % key] = '%s,%s' % (value,ip)

i = 0
hash = hashlib.md5()

print "{"
print '\t"data":['		
for k,v in result.iteritems():
    kv = {}
    hash.update(v.encode('utf-8'))    
    digest = hash.hexdigest()
    digest = digest[:2]+digest[10:12]+digest[30:32]
    k = digest + '_' + k
    port = k.split('-')[2]
    length = len(result)
    if i < length - 1 : 
    	print '''\t\t{"{#KEY_NAME}":"%s","{#HOSTLISTS}":"%s","{#PORT}":"%s"},''' % (k,v,port)
    else :
	print '''\t\t{"{#KEY_NAME}":"%s","{#HOSTLISTS}":"%s","{#PORT}":"%s"}''' % (k,v,port)
    i = i + 1
print '\t]'
print "}"
