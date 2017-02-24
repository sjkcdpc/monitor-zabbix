#!/usr/bin/env python
import os
import re
import sys
import xml.sax
import commands

class TCSerHandler(xml.sax.ContentHandler):
    def __init__(self):
        self._connectors = list()

    def startElement(self, tag, attributes):
        if tag == "Connector":
            protocal = attributes["protocol"]
            confitem = dict(attributes)
            self._connectors.append(confitem)

    def get_connectors(self):
        return self._connectors

    def get_biz_port(self):
        cons = self.get_connectors()
        for item in cons:
            protocol = item.get("protocol", None)
            if protocol == "HTTP/1.1":
                biz_port = item.get("port", None)
                return int(biz_port)
        return None

action = sys.argv[1]

local_ip="ip add|grep -E '10.0.1|10.0.2|192.168'|grep -v 127.0.0.1|awk '{print $2}'|awk -F / '{print $1}'"
local_ip=os.popen(local_ip).read().strip()
print local_ip

cmd1='find /usr/local/ -name server.xml'
result = os.popen(cmd1).read()
for line in result.split():
    cmd2='chmod 644 %s' % line
    print cmd2
    os.popen(cmd2)
    line1 = line.split('/server.xml')[0]
    cmd3='chown zabbix.zabbix %s' % line1
    print cmd3
    os.popen(cmd3)
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = TCSerHandler()
    parser.setContentHandler( handler )
    parser.parse(line)
    biz_port = int(handler.get_biz_port()) + 10000
    if commands.getoutput('ss -nlp|grep %s' % biz_port) != '' :
        print "error ---------------------------------------------------"
        os.exit(0)
    print biz_port
    path=line1.split('/conf')[0]
    dirname='%s/bin/catalina.sh' % path
    command = 'grep jmxremote %s' % dirname
    if action == 'delete' :
        scmd = "sed -i /'export CATALINA_OPTS=\"\$CATALINA_OPTS'/d %s" % dirname
        commands.getoutput(scmd)
        print commands.getoutput(command)

    elif action == 'check':
	print os.popen(command).read()

    elif action == 'add' :
        r = commands.getoutput(command)
        print r
        if r == '' :
            cmds='''
                sed -i '84a export CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote"'  %s
                sed -i '85a export CATALINA_OPTS="$CATALINA_OPTS -Djava.rmi.server.hostname=%s"' %s
                sed -i '86a export CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote.port=%s"' %s
                sed -i '87a export CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote.ssl=false"' %s
                sed -i '88a export CATALINA_OPTS="$CATALINA_OPTS  -Dcom.sun.management.jmxremote.authenticate=false"' %s
                ''' % (dirname,local_ip,dirname,biz_port,dirname,dirname,dirname)
            print cmds
            os.popen(cmds)

