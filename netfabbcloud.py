#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012, Miro Hrončok <miro@hroncok.cz>
# ISC license, see COPYING
# Chcecking the e-mails originaly form here: http://stackoverflow.com/a/6618585/1839451

import sys, re, urllib2, MultipartPostHandler, os.path, email, time
from datetime import datetime, timedelta
from imapclient import IMAPClient

## Put your config here
EMAIL = 'netfabbcloud@gmail.com'	# E-mail address
HOST = 'imap.gmail.com'				# IMAP server
USERNAME = EMAIL					# IMAP username
PASSWORD = '*******************'		# IMAP password
ssl = True							# Use SSL?
UNITS = 'mm'						# mm or inch
WAIT = 3							# How many secons wait between e-mail checks
verbose = False						# Display actions

## Chcek if we have exactly one argument
if len(sys.argv) != 2:
	print 'Usage: %s file.stl' % os.path.basename(sys.argv[0])
	exit(1)

## Check if the argument is file
if verbose: print 'Checking if the argument is file'
stlfile = sys.argv[1]
if not os.path.isfile(stlfile):
	print >> sys.stderr, '%s is not a file' % stlfile
	exit(1)

## Send the file to Netfabb Cloud
if verbose: print 'Sending the file to Netfabb Cloud...'
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
	print >> sys.stderr, e.reason
	exit(1)
if verbose: print '...sent.'

## It seems only english letters (low or capital), numbers and dots are left in the filename
crippledname = re.sub('[^0-9,a-z,A-Z,.]+', '', os.path.basename(stlfile))
if verbose: print 'Crippled name is %s' % crippledname

## Date stuff
today = datetime.today()
cutoff = today - timedelta(days=1)

try:
	## Let's find it
	go = True
	exitus = False
	while go:
		## Wait a bit
		time.sleep(WAIT)
		## Connect, login and select the INBOX
		if verbose: print 'Connecting to IMAP'
		server = IMAPClient(HOST, use_uid=True, ssl=ssl)
		server.login(USERNAME, PASSWORD)
		select_info = server.select_folder('INBOX')
		## Search for relevant messages
		messages = server.search(['FROM "cloud@netfabb.com"', 'SINCE %s' % cutoff.strftime('%d-%b-%Y')])
		## Fetch the messages
		if verbose: print 'Fetching e-mails...'
		response = server.fetch(messages, ['RFC822'])
		for msgid, data in response.iteritems():
			msg = data['RFC822']
			if verbose:
				mail = email.message_from_string(msg)
				print '...got e-mail: %s' % mail['Subject']
			## Processing/Success/Failure e-mail check
			if msg.find('"'+crippledname+'" was successfully uploaded to the system') > 0:
				if verbose: print 'This is a processing e-mail, just delete it'
				server.delete_messages(msgid)
			elif msg.find('Congratulations! Your uploaded file "'+crippledname+'" was processed successfully.') > 0:
				if verbose: print 'This is a success e-mail, got the URL'
				start = msg.find('?key=')
				end = msg.find('&fixedfile=1')
				url = 'http://cloud.netfabb.com/download.php'+msg[start:end]
				server.delete_messages(msgid)
				go = False # Don't break now, let this forloop end, so all messages are deleted
			elif msg.find('Unfortunately, your uploaded file "'+crippledname+'" was not processed successfully.') > 0:
				if verbose: print 'This is a failure e-mail'
				start = msg.find('The system logged the short error message')
				end = msg[start:].find('If you have further questions')
				print >> sys.stderr, msg[start:start+end-3] # -3 deletes whitesapce at the end
				server.delete_messages(msgid)
				exitus = True # Don't exit now, let this forloop end, so all messages are deleted
		if exitus: exit(1)
except IMAPClient.Error, e:
	print e
	exit(1)

## Get the download destination
fixedfile = ''.join(stlfile.split('.')[0:-1])+'_fixed.'+stlfile.split('.')[-1]
if verbose: print 'Will download to file %s' % fixedfile

## Donwload the file
try: remote = urllib2.urlopen(url)
except URLError, e:
	print >> sys.stderr, e.reason
	exit(1)
try:
	local = open(fixedfile, 'w')
	local.write(remote.read())
except IOError, e:
	print >> sys.stderr, 'IO Error'
	exit(1)
if verbose: print '...done'
remote.close()
local.close()
