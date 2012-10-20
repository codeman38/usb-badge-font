#!/usr/bin/env python

"""Renders text from an LCD font into the hex format used in
usb-badge-cli, and optionally, displays it to the screen."""
__author__='Cody "codeman38" Boisclair'
__email__='cody@zone38.net'
__version__='1.0'

import sys, argparse, os

_deffont_ = os.path.join(os.path.dirname(sys.argv[0]), 'fonts', 'ledbadge.lcd')

def main():
	parser = argparse.ArgumentParser(description='Displays text from an LCD font.')
	parser.add_argument('-f', dest='fontfile', required=False, default=_deffont_,
                        help='font file to use (default: %(default)s)')
	parser.add_argument('-v', dest='verbose', action='store_true',
						help='display line-by-line illustration of output')
	parser.add_argument('text', help='text to render')
	args = parser.parse_args()
	
	fontfile = open(args.fontfile)
	thefont = fontfile.read()
	fontfile.close()
	
	charbytes = process_font(thefont)
	outbytes = ''
	
	for ch in args.text:
		outbytes += charbytes[ord(ch)] + chr(0)
	outbytes = outbytes[:-1]
	
	outhex = ''
	for byte in outbytes:
		if args.verbose:
			bits = '{0:08b}'.format(ord(byte)).replace('0',' ').replace('1','#')
			bits = ''.join(reversed(bits))
			print '{0:3d} {1}'.format(ord(byte), bits)
		outhex += '{0:02x}'.format(ord(byte))
	
	if args.verbose:
		print
		print 'Hex encoding:'
	print outhex
		
def process_font(thefont):
	# first 32 characters are blank
	charbytes = [''] * 32

	pos = 0
	while pos < len(thefont):
		bytelen = ord(thefont[pos])
		pos += 1
		
		charbytes.append(thefont[pos:pos+bytelen])
		pos += bytelen

	return charbytes

if __name__=='__main__':
	main()
