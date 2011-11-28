# coding: utf8

import config as conf

__author__ = "rockosov@gmail.com"

def get_correct_texts( filename ):
	try:
		save = open( filename, "r" )
	except:
		print "Can't open file " + filename
		return []
	result = list()
	for line in save:
		res = line.split( " --- " )
		temp = list()
		for value in res:
			if value != '\r\n' and value != '':
				temp.append( value )
		result.append( temp )
	out = list()
	for i in range( 4 ):
		out.append( [] )
	index = 0
	while ( 1 ):
		if result[ index ] == []:
			break
		for i in range( 4 ):
			temp = result[ index ][ i ], result[ index + 1 ][ i ], result[ index + 2 ][ i ]
			out[i].append(temp)
		index += 4
	save.close()
	return out

def search():
	infoXL, infoXR, infoYL, infoYR = get_correct_texts( conf.FILENAME_COR_TEXTS )
	print infoXL
	print infoXR
	print infoYL
	print infoYR
	return 

if __name__ == "__main__":
	print "Sorry, this module hasn't main routine!\nPlease, call main.py!"
	
