#!/usr/bin/env python
import os
import sys
def getsum(port,key,ip):
    cmd = '/usr/local/zabbix/bin/zabbix_get -s %s -k mysql_stats[%s,%s]' % (ip,port,key)
    v = os.popen(cmd).read()
    return v

def main(port,key,hosts):
    result = 0
    for ip in hosts:
        r = getsum(port,key,ip)
        result = result + int(r)
    return result

if __name__ == '__main__' :
    port = sys.argv[1]
    key = sys.argv[2]
    hosts = sys.argv[3]
    hosts = hosts.split(',')
    result = main(port,key,hosts)
    print result
