#!/usr/bin/env python3

# Copyright 2017 Job Snijders <job@ntt.net>

import datetime
import fileinput
import json


def gt(dt_str):
    dt, _, us = dt_str.partition(".")
    dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    return dt.strftime("%Y%m%d")


def changed(dt_str):
    dt, _, us = dt_str[:-6].partition(".")
    dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    return dt.strftime("%Y%m%d")

input = ""

for line in fileinput.input():
    input += line

db = json.loads(input)

del input

stamp = gt(db['generation_date'])

for afi in ["v4", "v6"]:
    for entry in db['whois_records'][afi]:
        print("route{}: {}".format("6" if afi is "v6" else "", entry['prefix']))
        print("descr: {}".format(entry['name']))
        print("origin: {}".format(entry['originas']))
        print("remarks: This route object represents authoritative data retrieved from ARIN's WHOIS service.")
        print("remarks: The original data can be found here: {}".format(entry['ref']))
        print("remarks: This route object is the result of an automated WHOIS-to-IRR conversion process.")
        print("mnt-by: MAINT-JOB")
        print("changed: job@ntt.net {}".format(changed(entry['changed'])))
        print("source: {}".format(db['source']))
        print("")
