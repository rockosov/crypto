# coding = utf-8

__author__ = "rockosov@gmail.com"

import sys
sys.path.append( "../" )

import config as cfg
import bits_ops as bops
import algorithm

def add_bit_in_possible_keys( bit, bit_num, possible_keys ):
	if possible_keys == []:
		if bit == ".":
			possible_keys.append( 0 )
			possible_keys.append( 0 )
			possible_keys[ 0 ] = bops.set_bit( possible_keys[ 0 ], cfg.KEY_SIZE - bit_num, 0)
			possible_keys[ 1 ] = bops.set_bit( possible_keys[ 1 ], cfg.KEY_SIZE - bit_num, 1 )
		else:
			possible_keys.append( 0 )
			possible_keys[ 0 ] = bops.set_bit( possible_keys[ 0 ], cfg.KEY_SIZE - bit_num, int( bit, 10 ) )
	else:
		if bit == ".":
			possible_keys *= 2
			for i in range( len( possible_keys ) / 2 ):
				possible_keys[ i ] = bops.set_bit( possible_keys[ i ], cfg.KEY_SIZE - bit_num, 0 )
			for i in range( len( possible_keys ) / 2, len( possible_keys ) ):
				possible_keys[ i ] = bops.set_bit( possible_keys[ i ], cfg.KEY_SIZE - bit_num, 1 )
		else:
			for i in range( len( possible_keys ) ):
				possible_keys[ i ] = bops.set_bit( possible_keys[ i ], cfg.KEY_SIZE - bit_num, int( bit, 10 ))
			
	return possible_keys

def search_right_key( text ):
	key = 0
	possible_keys = list()
	print "Please, input key's bits:"
	for i in range( cfg.KEY_SIZE ):
		print "K" + str( i + 1 ) + ":",
		current_bit = raw_input()
		possible_keys = add_bit_in_possible_keys( current_bit, i + 1, possible_keys )
	
	plain_text, cipher_text = text

	print len( possible_keys )

	for current_key in possible_keys:
			current_cipher_text = algorithm.encrypt( plain_text, current_key )
			if current_cipher_text == cipher_text:
				key = current_key
				print key
	return key

def main():
	print "This module hasn't main call!"
	return

if __name__ == "__main__":
	sys.exit( main() )
