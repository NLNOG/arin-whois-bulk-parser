'''
Created on Nov 9, 2017

Usage: call script <format: 'json' or 'irr'> <xml source>

@author: arjan
@ook in geharkt: job
'''

import fileinput
import netaddr
import re
import datetime
import json
import sys

def gt(dt_str):
    dt = datetime.datetime.strptime(dt_str[:-6], "%Y-%m-%dT%H:%M:%S")
    return dt.strftime("%Y%m%d")

outputFormat = sys.argv[1]
if not (outputFormat == 'json' or 'irr'):
    print 'unknown output format'
    exit(2)

pCidrLength = re.compile('<cidrLenth>(.+?)<\/cidrLenth>')
pref = re.compile('<ref>(.+?)<\/ref>')
pupdateDate = re.compile('<updateDate>(.+?)<\/updateDate>')
pStartAddress = re.compile('<startAddress>(.+?)<\/startAddress>\s*</netBlock>')
pOriginAS = re.compile('<originAS>(.+?)<\/originAS>')

record = ''
linenr = 0

v4records = []
v6records = []
for line in fileinput.input(sys.argv[2:]):
    linenr += 1
    record += line
    if line == '</net>\n':
        mCidrLength = pCidrLength.findall(record)
        mupdateDate = pupdateDate.findall(record)[0]
        mref = pref.findall(record)[0].replace("/v1/", "/")
        mStartAddress = pStartAddress.findall(record)
        mOriginAS = pOriginAS.findall(record)
        if not mOriginAS is None:
            for vAS in mOriginAS:
                x = 0
                for vAddress in mStartAddress:
                    if int(mCidrLength[x]) > 24 and not ':' in vAddress:
                        continue
                    if int(mCidrLength[x]) > 48 and ':' in vAddress:
                        continue
                    pfx = netaddr.IPNetwork(vAddress + '/' + mCidrLength[x])
                    if outputFormat == 'irr':
                        if pfx.version == 4:
                            print "route: %s" % str(pfx)
                        else:
                            print "route6: %s" % str(pfx)
                        print "descr: %s" % mref.split('/')[-1]
                        print "remarks: %s" % mref
                        print "origin: AS%s" % vAS
                        print "changed: nobody@nlnog.net %s" % gt(mupdateDate)
                        print "source: ARIN-WHOIS"
                        print ""
                    elif outputFormat == 'json':
                        d = {}
                        d['prefix'] = str(pfx)
                        d['originas'] = 'AS%s' % vAS
                        d['ref'] = '%s' % mref
                        d['name'] = '%s' % mref.split('/')[-1]
                        d['changed'] = mupdateDate
                        if pfx.version == 4:
                            v4records.append(d)
                        else:
                            v6records.append(d)
                    x += 1
        record = ''
if outputFormat == 'json':
    arin = {}
    arin['generation_date'] = datetime.datetime.utcnow().isoformat()
    arin['whois_records'] = {}
    arin['whois_records']['v4'] = v4records
    arin['whois_records']['v6'] = v6records
    arin['json_schema'] = '0.0.3'
    arin['source'] = 'ARIN-WHOIS'
    arin['help'] = 'http://teamarin.net/2016/07/07/origin-as-an-easier-way-to-validate-letters-of-authority/'
    print json.dumps(arin, sort_keys=True, indent=4)

