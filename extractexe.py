#!/usr/bin/env python

import sys, argparse
from os import path

"""Extracts the font from Inland's original LED badge driver EXE."""
__author__='Cody "codeman38" Boisclair'
__email__='cody@zone38.net'
__version__='1.0'

# Magic number locations from Inland's original EXE
_startloc_ = 0x133F40
_endloc_ = 0x134F6C

def main():
	parser = argparse.ArgumentParser(description='Extracts the font from Inland\'s original driver EXE.')
	parser.add_argument('infile', help='input font filename', nargs='?', default='ledbadge.exe')
	parser.add_argument('outfile', nargs='?', help='output font filename', default='ledbadge.lcd')
	args = parser.parse_args()

	chardata = {}

	fd = open(args.infile, 'rb')
	# Starting location in file is 133F40
	fd.seek(_startloc_, 0)
	
	max_char = 0
	
	while fd.tell() < _endloc_:
		thisdata = fd.read(18)
		asciival = ord(thisdata[0]) + ord(thisdata[1]) * 0x100
		if asciival > max_char: max_char = asciival
		numbytes = ord(thisdata[2])
		print 'Char {0}: {1} bytes'.format(asciival, numbytes)
		outdata = chr(numbytes) + thisdata[3:3+numbytes]
		# Save space - output zero width for blank non-space chars
		if asciival == 32 or not allzero(outdata[1:]):
			chardata[asciival] = outdata
	
	outfname = args.outfile
	outfd = open(outfname, 'wb')
	for x in range(32, max_char+1):
		if x in chardata:
			outfd.write(chardata[x])
		else:
			outfd.write(chr(0))
	outfd.close()

def allzero(data):
	for ch in data:
		if ch != chr(0):
			return False
	return True

if __name__=='__main__':
	main()
	