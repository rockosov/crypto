# coding: utf8

__author__ = "rockosov@gmail.com"

def get_bit( source, position ):
	return ( source >> position ) & 1

def set_bit( destination, position, bit ):
	return destination | ( bit << position )
