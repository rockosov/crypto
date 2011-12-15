# coding: utf8

__author__ = "rockosov@gmail.com"

import sys
sys.path.append( "../" )

import search_characteristic as sc
import search_keys as sk
import bits_ops as bops
import config as cfg

def main():
	print "Try to search characteristic..."
	search_result = sc.search()
	print "DONE!\n"
	print "Try to search keys..."
	keys = sk.search( search_result )
	print "DONE!"
	print "Try to search right key..."
	key = sk.search_right_key( keys )
	print "DONE!"
	print "Right key is", bops.full_bin( key, cfg.KEY_SIZE )

if __name__ == "__main__":
	sys.exit(main())
