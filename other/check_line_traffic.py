#!/usr/bin/env python
#-*- coding:utf8 -*-
import MySQLdb
import sys
import os
import time
 
#tosms=['15210491149','13811578206','13466345915']
tosms=['15210491149']
percent = 0.4

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
        result = results[0]
    except:
	result = [0,0]
    return  result
    cur.close()
    conn.close()

def genkey(port):
    key='ifInOctets[%s]' % (port) 
    return key

def gencmd(ip,key):
    sql='''
        select value,clock from history_uint  where itemid=(
        select itemid from items where  key_="%s" and hostid=
        (select hostid from interface where ip='%s'))
        order by clock desc   limit 1
        '''  % (key,ip)
    return sql

def main():
    root_path = os.path.dirname(__file__)
    result = open('%s/line.txt' % root_path,'r')
    for line in result.readlines():
	list = line.split()
	linename = list[0]
	ip = list[1]
	port = list[2]
	total_traffic = int(list[3]) * 1024 * 1024
	trigger = total_traffic * float(percent)
	key = genkey(list[2])
	sql = gencmd(ip,key)
        result = conndb(sql)
	v = result[0]
	clock = result[1]
	content = ''
	print v,clock
	if v >= trigger :
	    title = "专线报警"
	    print linename
	    content = "专线" + linename + "超过报警流量阀值\(带宽的80%\)"
	    for sms in tosms :
	    	os.popen('php sms.php %s %s' % (sms,content)).read()

	time_local = time.localtime(clock)
	dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
	file = open('%s/checklog.txt' % root_path ,'a')
	now_traffic = '%.2f' % (v/1024) + 'kbps'
	str = "专线%s:	%s 流量为%s\t%s\n" % (linename,dt,now_traffic,content)
	file.write(str)

if __name__ == '__main__':
    main()
