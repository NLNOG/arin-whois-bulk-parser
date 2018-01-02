all:	fetch load

fetch:
	rm arin-whois-originas.json
	wget -q -O arin-whois-originas.json.bz2 http://irrexplorer.nlnog.net/static/dumps/arin-whois-originas.json.bz2
	bunzip2 arin-whois-originas.json.bz2
	cat arin-whois-originas.json | python convert-arin-whois.py > arin-whois.db
	# check if the size of the output file makes any sense
	if [ $(shell wc -l arin-whois.db  | cut -f1 -d" ") -lt 500000 ] ; then \
		exit 1; \
	fi
	irr_rpsl_check -c -f ./arin-irrd.conf -o arin-whois.db.tmp arin-whois.db > /dev/zero
	mv arin-whois.db.tmp arin-whois.db
	echo $(shell expr `cat ARIN-WHOIS.CURRENTSERIAL` + 1) > ARIN-WHOIS.CURRENTSERIAL

load:
	cp arin-whois.db /var/tmp/
	cp ARIN-WHOIS.CURRENTSERIAL /home/irrd/db/
	./signal-load.bash
