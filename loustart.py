#!/usr/bin/python

from loungetable import *

table = LoungeTable("111","360","150","150")
table.startTable()

while True:
	try:
		pass
	except:
		table.running = False
		table.stopTable()