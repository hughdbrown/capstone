ALL: \
	urlhist-timestamp-de-es-it-us.json \
	urlhist-timestamp-ca-us.json


urlhist-US-DE-ES-IT.json:
	cd script
	./extract-US-DE-ES-IT-urls.sh

urlhist-US-CA.json:
	cd script
	./extract-US-CA.urls.sh
