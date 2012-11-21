#!/usr/bin/env bash

USAGE="Usage: $0 file.stl [mm|inch]"


curl --form file="$file" --form email="$email" --form units="$units" \
	--form filerepair=1 --form termsandconditions=1 --form upload="Upload to Cloud" \
	http://cloud.netfabb.com/index.php > /dev/null
