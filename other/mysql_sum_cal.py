#!/usr/bin/env python
import MySQLdb
import sys
import os
def conndb(command):
    conn = MySQLdb.connect(host='localhost',
                           user="root",
                           passwd="51talk.com",
                           db="zabbix",
                           unix_socket='/tmp/mysql.sock')
    cur = conn.cursor()
    cur.execute('%s;' % command)
    results = cur.fetchall()
    try:
        result = results[0][0]
    except:
	result = 0
    return  result
    cur.close()
    conn.close()

def genkey(port,key):
    newkey='mysql_stats[%s,%s]' % (port,key) 
    return newkey

def gencmd(ip,key):
    sql='''
        select value from history_uint  where itemid=(
        select itemid from items where  key_="%s" and hostid=
        (select hostid from interface where ip='%s'))
        order by clock desc   limit 1
        '''  % (key,ip)
    return sql

def main():
    port = sys.argv[1]
    key = sys.argv[2]
    hosts = sys.argv[3]
    key = genkey(port,key)
    hosts = hosts.split(',')
    sum = 0
    for ip in hosts:
        command = gencmd(ip,key)
        v = conndb(command)
        sum = sum + int(v)
    return sum

if __name__ == '__main__':
    r = main()
    print r
