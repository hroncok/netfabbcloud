#!/usr/bin/env bash

USAGE="Usage: $0 file.stl [mm|inch]"

email="`cat $HOME/.config/netfabbcloud/email 2>/dev/null`"
username="`cat $HOME/.config/netfabbcloud/username 2>/dev/null`"
password="`cat $HOME/.config/netfabbcloud/password 2>/dev/null`"
imap="`cat $HOME/.config/netfabbcloud/imap 2>/dev/null`"
units="`cat $HOME/.config/netfabbcloud/units 2>/dev/null`"

# Check the values and dispaly info
if [ -z $email ] || [ -z $units ] || [ -z $password ] || [ -z $imap ]; then
	echo "Set your e-mail address, password, IMAP and units first."
	echo
	echo "Your e-mail password will be stored as text,"
	echo " it's recomanded to use special mailbox just for this."
	echo
	echo "To set your setting, run:"
	echo
	echo "mkdir -p ~/.config/netfabbcloud"
	echo "echo foo@bar.tld > ~/.config/netfabbcloud/email"
	echo "echo notsosecretpassword > ~/.config/netfabbcloud/password"
	echo "echo imap.foo.tld > ~/.config/netfabbcloud/imap"
	echo "echo mm > ~/.config/netfabbcloud/units"
	echo
	echo "Available units are mm or inch"
	echo
	echo "If your IMAP username differs your e-mail adress, set it too:"
	echo
	echo "echo foo > ~/.config/netfabbcloud/username"
	exit 1
fi

# Use e-mail address as username if username not set
if [ -z $username ]; then
	username=email
fi

# no file -> no run
if [ -z "$1" ]; then
	echo $USAGE
	exit 1
fi

if [ ! -f "$1" ]; then
	echo "$1 is not a file!"
	exit 1
fi

# Got the file
file="$1"

curl --form file="$file" --form email="$email" --form units="$units" \
	--form filerepair=1 --form termsandconditions=1 --form upload="Upload to Cloud" \
	http://cloud.netfabb.com/index.php > /dev/null
if [ $? > 0 ]; then
	echo "Cannot send file via curl"
	exit 1
fi

rundir="`dirname "$0"`"
rawmails="`$rundir/getmail.py 2>/dev/null`"
if [ $? > 0 ]; then
	echo "Cannot get mail, check your login details stored in ~/.config/netfabbcloud"
	exit 1
fi
