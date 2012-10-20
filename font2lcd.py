#!/usr/bin/env python

"""Converts a standard NES-formatted bitmap font into an LCD font,
for use with the Inland USB name badge."""
__author__='Cody "codeman38" Boisclair'
__email__='cody@zone38.net'
__version__='1.0'

import sys, argparse
from os import path

_downshift_ = 1
_spacewidth_ = 3

def main():
	parser = argparse.ArgumentParser(description='Converts a standard NES-formatted bitmap font to an LCD font.')
	parser.add_argument('infile', help='input font filename')
	parser.add_argument('outfile', nargs='?', help='output font filename')
	args = parser.parse_args()
	
	fd = open(args.infile, 'rb')
	
	num_chars = 0
	outbytes = ''
	while True:
		chbytes = fd.read(8)
		if len(chbytes) < 8:
			break
		outbytes += reformat(chbytes)
		
	if len(sys.argv) > 2:
		outfname = args.outfile
	else:
		outfname = path.splitext(args.infile)[0]+'.lcd'
	
	outfd = open(outfname, 'wb')
	outfd.write(outbytes)
	outfd.close()
	
def reformat(bytes):
	# Transpose the bytes
	trans = transpose(bytes)
	
	# Remove all spacing around it...
	while len(trans) > 0 and trans[0] == chr(0):
		trans = trans[1:]
	while len(trans) > 0 and trans[-1] == chr(0):
		trans = trans[:-1]
	
	# Add one pixel space, or _spacewidth_ if character is empty
	if len(trans) == 0:
		trans = chr(0) * (_spacewidth_-1)
	
	trans = chr(len(trans)) + trans
	return trans

def transpose(bytes):
	bytesbin = ['{0:08b}'.format(ord(x)) for x in bytes]
	transbin = zip(*bytesbin)
	trans = ''.join([chr(eval('0b'+''.join(x))>>_downshift_) for x in transbin])
	return trans

if __name__=='__main__':
	main()
	
