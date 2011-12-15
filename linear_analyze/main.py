# coding=utf-8

__author__ = "rockosov@gmail.com"

import sys

import search_statistics as ss
import search_analogs as sa
import search_key_equations as ske
import search_key as skey
import config as cfg
import bits_ops as bops

def main():
	statistics = ss.search()
	analogs = sa.search( statistics )
	equations = ske.search( analogs )

	print "Keys Equations:"
	for i in equations:
		for j in range( len( i[ 0 ] ) ):
			print "K" + str( i[ 0 ][ j ] ),
			if j != len( i[ 0 ] ) - 1:
				print "+",
		print "= " + str( i[ 1 ] )

	texts = ske.get_texts( cfg.FILENAME_COR_TEXTS )

	key = bops.full_bin( skey.search_right_key( texts[ 0 ] ), cfg.KEY_SIZE )
	print "Key is:", key

	return

if __name__ == "__main__":
	sys.exit( main() )
