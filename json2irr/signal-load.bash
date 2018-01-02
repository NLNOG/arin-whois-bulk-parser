#!/usr/bin/env bash

exec 2>> /dev/stdout

set -ev

exec 3<>/dev/tcp/rr.ntt.net/43
echo -e '!BARIN-WHOIS' >&3
grep -q C <&3
