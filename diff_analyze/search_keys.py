# coding: utf8

import config as conf
import bits_ops

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
			temp = int( result[ index ][ i ], 2 ), \
				int( result[ index + 1 ][ i ], 2 ), \
				int( result[ index + 2 ][ i ], 2 )
			out[i].append(temp)
		index += 4
	save.close()
	return out

def search_valid_pairs( dA, dC, block ):
	result = list()
	for a1 in range( 16 ):
		a2 = dA ^ a1
		# посчитаем c1 и c2
		c1 = block.substitution( a1 )
		c2 = block.substitution( a2 )
		# вычислим delta_c
		dc = c1 ^ c2
		# запомним
		if dc == dC:
			result.append( ( a1, a2 ) )
	return result
			

def search_k1( general_data, info ):
	f_block, s_block, t_block, E_perm, P_perm = general_data

	infoXL, infoXR = info[ :2 ]

	for index in range( len( infoXL ) ):
		dD = infoXL[ index ][ 2 ]
		dC = P_perm.make_permutation( dD, -1 )
		dXR = infoXR[ index ][ 2 ]
		dA = E_perm.make_permutation( dXR, 1 )
		XR = infoXR[ index ][ 0 ]

		for i in range( 3 ):
			if i == 0:
				dCi = bits_ops.get_bits( dC, i * 2, 2 )
				current_block = f_block
			elif i == 1:
				current_block = s_block
				dCi = bits_ops.get_bits( dC, i * 2, 3 )
			else:
				current_block = t_block
			dAi = bits_ops.get_bits( dA, i * 4, 4 )
			XRi = bits_ops.get_bits( XR, i * 3, 3 )

			possible = search_valid_pairs( dAi, dCi, current_block )
	
def search_k3( general_data, info ):
	return


def search( general_data ):
	info = get_correct_texts( conf.FILENAME_COR_TEXTS )

	K = ""

	K1 = search_k1( general_data, info )
	K3 = search_k3( general_data, info )

#	K = K1 + K3

	print K

	return 

if __name__ == "__main__":
	print "Sorry, this module hasn't main routine!\nPlease, call main.py!"
	
