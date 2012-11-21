#!/usr/bin/env python
import sys
from datetime import datetime, timedelta
import email
from imapclient import IMAPClient

## http://stackoverflow.com/a/6618585/1839451
## Put your info here
EMAIL = "netfabbcloud@gmail.com"
HOST = "imap.gmail.com"
USERNAME = EMAIL
PASSWORD = "******************"
ssl = True

today = datetime.today()

## Connect, login and select the INBOX
server = IMAPClient(HOST, use_uid=True, ssl=ssl)
server.login(USERNAME, PASSWORD)
select_info = server.select_folder('INBOX')

## Search for relevant messages
messages = server.search(['FROM "cloud@netfabb.com"', 'SINCE %s' % today.strftime('%d-%b-%Y')])
response = server.fetch(messages, ['RFC822'])

for msgid, data in response.iteritems():
	msg_string = data['RFC822']
	msg = email.message_from_string(msg_string)
	#print '%s' % (msg['text'])
	print msg
