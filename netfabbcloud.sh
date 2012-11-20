#!/usr/bin/env bash

USAGE="Usage: $0 file.stl [mm|inch]"

email="`cat $HOME/.config/netfabbcloud/email 2>/dev/null`"
#password="`cat $HOME/.config/netfabbcloud/password 2>/dev/null`"
units="`cat $HOME/.config/netfabbcloud/units 2>/dev/null`"

#  || [ -z $password ]

if [ -z $email ] || [ -z $units ]; then
	echo "Set your e-mail address, password and units first."
	echo
	echo "Your e-mail password will be stored as text,"
	echo " it's recomanded to use special mailbox just for this."
	echo
	echo "To set your setting, run:"
	echo
	echo "mkdir -p ~/.config/netfabbcloud"
	echo "echo foo@bar.tld > ~/.config/netfabbcloud/email"
	echo "echo notsosecretpassword > ~/.config/netfabbcloud/password"
	echo "echo mm > ~/.config/netfabbcloud/units"
	echo
	echo "Available units are mm or inch"
	echo "Password is yet unused and doesn't neet to be set"
	exit 1
fi

if [ -z "$1" ]; then
	echo $USAGE
	exit 1
fi

file="$1"

curl --form file="$file" --form email="$email" --form units="$units" \
	--form filerepair=1 --form termsandconditions=1 --form upload="Upload to Cloud" \
	http://cloud.netfabb.com/index.php > /dev/null
