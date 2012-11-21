#!/usr/bin/env python

import sys, re, urllib2, MultipartPostHandler, os.path, email
from datetime import datetime, timedelta
from imapclient import IMAPClient

## Chcek if we have exactly one argument
if len(sys.argv) != 2:
	print 'Usage: %s file.stl' % sys.argv[0]
	exit(1)

## Check if the argument is file
stlfile = sys.argv[1]
if not os.path.isfile(stlfile):
	print '%s is not a file' % stlfile
	exit(1)

## Put your info here
EMAIL = 'netfabbcloud@gmail.com'
HOST = 'imap.gmail.com'
USERNAME = EMAIL
PASSWORD = '******************'
ssl = True
UNITS = 'mm'

## Send the file to Netfabb Cloud
url = 'http://cloud.netfabb.com/index.php'
data = {}
data['file'] = open(stlfile, 'rb')
data['email'] = EMAIL
data['units'] = UNITS
data['filerepair'] = '1'
data['termsandconditions'] = '1'
data['upload'] = 'Upload to Cloud'
opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
urllib2.install_opener(opener)
request = urllib2.Request(url, data)
try: page = urllib2.urlopen(request)
except URLError, e:
	print e.reason
	exit(1)

## It seems only english letters (low or capital), numbers and dots are left in the filename
crippledname = re.sub('[^0-9,a-z,A-Z,.]+', '', stlfile)

try:
	## Connect, login and select the INBOX
	server = IMAPClient(HOST, use_uid=True, ssl=ssl)
	server.login(USERNAME, PASSWORD)
	select_info = server.select_folder('INBOX')
	## Search for relevant messages
	messages = server.search(['FROM "cloud@netfabb.com"', 'SINCE %s' % datetime.today().strftime('%d-%b-%Y')])
	response = server.fetch(messages, ['RFC822'])

	for msgid, data in response.iteritems():
		msg_string = data['RFC822']
		msg = email.message_from_string(msg_string)
		print '%s' % msg['Subject']
		#print msg
except IMAPClient.Error, e:
	print e
	exit(1)

## Error string:
# Unfortunately, your uploaded file "FILE" was not processed successfully. The system logged the short error message "ERROR".
## OK string:
# Congratulations! Your uploaded file "FILE" was processed successfully. The results are located at
