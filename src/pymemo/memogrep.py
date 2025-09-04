# -*- coding: euc-jp -*-

import sys
import re

BUFSIZE = 64*1024

def memogrep(fpathname, pattern):

	matchlinelist = __search(fpathname, pattern)
	return matchlinelist

def __search(fpathname, pattern):
	reflags = 0
	matchlines = []
	reflags = reflags | re.IGNORECASE #| re.LOCALE
	try:
		#pattern = pattern.encode('utf-8')
		prog = re.compile(pattern, reflags)
	except re.error:
		print("Error: Bad regular expression %s" % pattern)
		return []
	try:
		f = open(fpathname)
	except IOError:
		print("Error: Can't open file %s" % fpathname)
		return []
	f.seek(0, 2)
	pos = f.tell()
	leftover = None
	while pos > 0:
		size = min(pos, BUFSIZE)
		pos = pos - size
		f.seek(pos)
		buffer = f.read(size)
		lines = buffer.split("\n")
		del buffer
		if leftover is None:
			if not lines[-1]:
				del lines[-1]
		else:
			lines[-1] = lines[-1] + leftover
		if pos > 0:
			leftover = lines[0]
			del lines[0]
		else:
			leftover = None
		lines.reverse()
		for line in lines:
			if prog.search(line):
				matchlines.append(line)
	return matchlines
