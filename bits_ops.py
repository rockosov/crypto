# coding: utf8

__author__ = "rockosov@gmail.com"

def get_bit( source, position ):
	return ( source >> position ) & 1

def set_bit( destination, position, bit ):
	if bit == 1:
		return destination | ( bit << position )
	else:
		mask = 0
		for i in range( len( bin( destination ).lstrip( "0b" ) ) ):
			if i == position:
				continue
			mask += 1 << i
		return destination & mask 

def get_bits( source, position, num ):
	mask = 0
	for i in range( num ):
		mask += 1 << i
	return ( source >> position ) & mask
