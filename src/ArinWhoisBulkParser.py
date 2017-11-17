'''
Created on Nov 9, 2017

@author: arjan
@ook in geharkt: job
'''

import fileinput
import netaddr
import re

pCidrLength = re.compile('<cidrLenth>(.+?)<\/cidrLenth>')
pStartAddress = re.compile('<startAddress>(.+?)<\/startAddress>\s*</netBlock>')
pOriginAS = re.compile('<originAS>(.+?)<\/originAS>')

record = ''
linenr = 0

for line in fileinput.input():
    linenr += 1
    record += line
    if line == '</net>\n':
        mCidrLength = pCidrLength.findall(record)
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
                    if pfx.version == 4:
                        print "route: %s" % str(pfx)
                    else:
                        print "route6: %s" % str(pfx)
                    print "origin: AS%s" % vAS
                    print "source: ARIN-WHOIS"
                    print ""
                    x += 1
        record = ''