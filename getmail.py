#!/usr/bin/env python
import sys
from datetime import datetime, timedelta
import email
from imapclient import IMAPClient

print sys.argv[1]
print sys.argv[2]

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
HOST = sys.argv[3]
ssl = True

today = datetime.today()
cutoff = today - timedelta(days=5)

## Connect, login and select the INBOX
server = IMAPClient(HOST, use_uid=True, ssl=ssl)
server.login(USERNAME, PASSWORD)
select_info = server.select_folder('INBOX')

## Search for relevant messages
messages = server.search(['FROM "cloud@netfabb.com"', 'SINCE %s' % cutoff.strftime('%d-%b-%Y')])
response = server.fetch(messages, ['RFC822'])

for msgid, data in response.iteritems():
	msg_string = data['RFC822']
	msg = email.message_from_string(msg_string)
	#print '%s' % (msg['text'])
	print msg
