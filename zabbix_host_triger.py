#!/usr/bin/env python
#coding:utf8

'''
Created on 03.06.2015
'''

import optparse
import sys
import traceback
from getpass import getpass
from core import ZabbixAPI

def get_options():
    usage = "usage: %prog [options]"
    OptionParser = optparse.OptionParser
    parser = OptionParser(usage)

    parser.add_option("-s","--server",action="store",type="string",\
        dest="server",help="(REQUIRED)Zabbix Server URL.")
    parser.add_option("-u", "--username", action="store", type="string",\
        dest="username",help="(REQUIRED)Username (Will prompt if not given).")
    parser.add_option("-p", "--password", action="store", type="string",\
        dest="password",help="(REQUIRED)Password (Will prompt if not given).")
    parser.add_option("-H","--hostname",action="store",type="string",\
        dest="hostname",help="(REQUIRED)hostname for hosts.")
    parser.add_option("--url",action="store",type="string",\
        dest="url",default="",help="http test URL ")
    parser.add_option("--headerhost",action="store",type="string",\
        dest="headerhost",default="",help="httptest step  header ")
    parser.add_option("--httptestname",action="store",type="string",\
        dest="httptestname",default="",help="""http test name ")
Possible values are:
0 - (default) monitored host;
1 - unmonitored host.""")
    parser.add_option("-f","--file",dest="filename",\
        metavar="FILE",help="Load values from input file. Specify - for standard input Each line of file contains whitespace delimited: <hostname>4space<ip>4space<groups>4space<templates>")

    options,args = parser.parse_args()

    if not options.server:
        options.server = raw_input('server http:')

    if not options.username:
        options.username = raw_input('Username:')

    if not options.password:
        options.password = getpass()

    return options, args

def errmsg(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(-1)

if __name__ == "__main__":
    options, args = get_options()

    zapi = ZabbixAPI(options.server,options.username, options.password)

    hostname = options.hostname
    httptestname = options.httptestname
    headerhost = options.headerhost
    url = options.url
    hostid=zapi.host.get({"filter":{"host":hostname}})[0]["hostid"]
    try:
        if url:
            description="访问"+httptestname+"出现问题,探测IP："+ url
            expression="{"+"Zabbix-Server:web.test.fail["+httptestname+"].last()"+"}"+"<>0 and " + "{"+"bj8-cmcdn0.bjcsk.cmcdn.net:web.test.fail["+httptestname+"].last()"+"}"+"<>0 and "  + "{"+"gd4-cmcdn1.gdyj.cmcdn.net:web.test.fail["+httptestname+"].last()"+"}"+"<>0 and " + "{"+"hb4-cmcdn1.hbwh.cmcdn.net:web.test.fail["+httptestname+"].last()"+"}"+"<>0 and "+ "{"+"nm2-cmcdn0.nmyd.cmcdn.net:web.test.fail["+httptestname+"].last()"+"}"+"<>0 and "+ "{"+"xz3-cmcdn1.xzyd.cmcdn.net:web.test.fail["+httptestname+"].last()"+"}"+"<>0"
	    print expression
            print zapi.trigger.create({"description":description,"expression":expression,"priority":5})
	else:
            print zapi.httptest.create({"name":httptestname,"hostid":hostid,"steps":[{"name": httptestname,"url": url,"status_codes": "200","required":"successed","headers":[{"Host":headerhost}],"no": 1}]})
    except Exception as e:
	    print str(e)
