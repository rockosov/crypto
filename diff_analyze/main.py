# coding: utf8

__author__ = "rockosov@gmail.com"

import search_characteristic as sc
import search_keys as sk
import sys

def main():
	print "Try to search characteristic..."
	sc.search()
	print "DONE!\n"
	print "Try to search keys..."
	sk.search()
	print "DONE!"

if __name__ == "__main__":
	sys.exit(main())
