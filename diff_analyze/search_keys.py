# coding: utf8

import sys

sys.path.append( "../" )

import config as conf
import bits_ops
import algorithm

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

def get_keys( possible, EIn, keys ):
	for value in possible:
		cur_key = value[ 0 ] ^ EIn
		keys[ cur_key ] += 1
	return keys

def search_k( general_data, infoIn, infoOut ):
	f_block, s_block, t_block, E_perm, P_perm = general_data

	result_keys = [ list(), list(), list() ]
	for i in range( 3 ):
		result_keys[ i ] = range( 16 )
		for j in range( len( result_keys[ i ] ) ):
			result_keys[ i ][ j ] = 0
	for index in range( len( infoOut ) ):
		dD = infoOut[ index ][ 2 ]
		dC = P_perm.make_permutation( dD, -1 )
		dIn = infoIn[ index ][ 2 ]
		dA = E_perm.make_permutation( dIn, 1 )
		In = infoIn[ index ][ 0 ]
		EIn = E_perm.make_permutation( In, 1 )

		for i in range( 3 ):
			if i == 0:
				dCi = bits_ops.get_bits( dC, conf.HALF_BLOCK_SIZE - 3, 3 )
				current_block = f_block
			elif i == 1:
				current_block = s_block
				dCi = bits_ops.get_bits( dC, conf.HALF_BLOCK_SIZE - 6, 3 )
			else:
				current_block = t_block
				dCi = bits_ops.get_bits( dC, 0, 2 )
			dAi = bits_ops.get_bits( dA, conf.EXT_HALF_BLOCK_SIZE - ( i + 1 ) * 4, 4 )
			possible = search_valid_pairs( dAi, dCi, current_block )
			EIni = bits_ops.get_bits( EIn, conf.EXT_HALF_BLOCK_SIZE - ( i + 1 ) * 4, 4 )
			result_keys[ i ] = get_keys( possible, EIni, result_keys[ i ] )
	return result_keys

def get_max_possible_keys( keys ):
	for index in range( len( keys ) ):
		current_max = max( keys[ index ] )
		temp_list_max = list()
		for i in range( len( keys[ index ] ) ):
			if keys[ index ][ i ] == current_max:
				temp_list_max.append( i )
		keys[ index ] = temp_list_max
	result_keys = list()
	for i in keys[ 0 ]:
		for j in keys[ 1 ]:
			for k in keys[ 2 ]:
				result_keys.append( ( i << 8 ) | ( j << 4 ) | ( k ) )
	return result_keys

def form_possible_keys( K1, K3 ):
	result_keys = list()
	for i in K1:
		for j in K3:
			result_keys.append( ( i << 12 ) | ( j ) )
	return result_keys
	
def search( general_data ):
	infoXL, infoXR, infoYL, infoYR = get_correct_texts( conf.FILENAME_COR_TEXTS )

	K1 = search_k( general_data, infoXR, infoXL )
	K3 = search_k( general_data, infoYR, infoYL )

	K1 = get_max_possible_keys( K1 )
	K3 = get_max_possible_keys( K3 )

	K = form_possible_keys( K1, K3 )

	return K

def search_right_key( keys ):
	infoXL, infoXR, infoYL, infoYR = get_correct_texts( conf.FILENAME_COR_TEXTS )

	plain_text = ( infoXL[ 0 ][ 0 ] << conf.HALF_BLOCK_SIZE ) | ( infoXR[ 0 ][ 0 ] )
	cipher_text = ( infoYL[ 0 ][ 0 ] << conf.HALF_BLOCK_SIZE ) | ( infoYR[ 0 ][ 0 ] )
	
	print bin( infoXL[ 0 ][ 0 ] ), bin( infoXR[ 0 ][ 0 ] )
	print bin( plain_text )
	print bin( infoYL[ 0 ][ 0 ] ), bin( infoYR[ 0 ][ 0 ] )
	print bin( cipher_text )

	result_key = 0
	for current_key in  keys:
		current_cipher_text = algorithm.encrypt( plain_text, current_key )
		if current_cipher_text == cipher_text:
			result_key = current_key
			break
	if result_key == 0:
		print "Can't find right key!"

	return result_key

if __name__ == "__main__":
	print "Sorry, this module hasn't main routine!\nPlease, call main.py!"
