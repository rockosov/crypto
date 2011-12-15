# coding = utf-8

__author__ = "rockosov@gmail.com"

import sys
sys.path.append( "../" )

import blocks_internal
import bits_ops as bos

def get_analogs( with_alpha, with_beta, key_bits, stats ):
	left1 = list()
	left2 = list()
	right = list()
	with_alpha = with_alpha[ ::-1 ]
	with_beta = with_beta[ ::-1 ]
	key_bits = key_bits[ ::-1 ]
	out = list()
	for stat in stats:
		left1 = list()
		left2 = list()
		right = list()
		for i in range( len( with_alpha ) ):
			current_bit = bos.get_bit( stat[ 0 ], i )
			if current_bit == 1:
				left1.append( with_alpha[ i ] )
				right.append( key_bits[ i ] )
		for i in range( len( with_beta ) ):
			current_bit = bos.get_bit( stat[ 1 ], i )
			if current_bit == 1:
				left2.append( with_beta[ i ] )
		result = left1, left2, right, stat
		out.append( result )
	return out

def convert_deap_list( target ):
	result = list()
	for i in target:
		for j in i:
			result.append( j )
	return result

def join_likelihood( p1, p2 ):
	return ( 1 - p1 - p2 + 2*p1*p2 )

def join_analogs( x, y ):
	result = list()
	for i in range( len( x ) ):
		left1 = x[ i ][ 0 ] + x[ i ][ 1 ]
		left2 = y[ i ][ 0 ] + y[ i ][ 1 ]
		right = x[ i ][ 2 ] + y[ i ][ 2 ]
		stat = x[ i ][ 3 ][ 0 ], x[ i ][ 3 ][ 1 ], join_likelihood( x[ i ][ 3 ][ 2 ], y[ i ][ 3 ][ 2 ] )
		result.append( ( left1, left2, right, stat ) )
	return result

def search( statistics ):
	fb_stat, sb_stat, tb_stat = statistics 
	E_perm = blocks_internal.Permutation_Internal( "E" )
	P_perm = blocks_internal.Permutation_Internal( "P" )
	EXR_bo = E_perm.make_permutation_in_bit_order( range( 9, 17 ), 1 )
	PC_bo = P_perm.make_permutation_in_bit_order( range( 1, 9 ), -1 )

	print "\nFIRST ROUND:"
	fr_fb_analogs = get_analogs( EXR_bo[ :4 ], convert_deap_list( PC_bo[ :3 ] ), range( 1, 5 ), fb_stat )
	fr_sb_analogs = get_analogs( EXR_bo[ 4:8 ], convert_deap_list( PC_bo[ 3:6 ] ), range( 5, 9 ), sb_stat )
	fr_tb_analogs = get_analogs( EXR_bo[ 8:12 ], convert_deap_list( PC_bo[ 6:8 ] ), range( 9, 13 ), tb_stat )
	print "\nFirst block, analogs:" 
	print fr_fb_analogs
	print "\nSecond block, analogs:"
	print fr_sb_analogs
	print "\nThird block, analogs:"
	print fr_tb_analogs
	
	print "\nTHIRD ROUND:"
	tr_fb_analogs = get_analogs( EXR_bo[ :4 ], convert_deap_list( PC_bo[ :3 ] ), range( 13, 17 ), fb_stat )
	tr_sb_analogs = get_analogs( EXR_bo[ 4:8 ], convert_deap_list( PC_bo[ 3:6 ] ), range( 17, 21 ), sb_stat )
	tr_tb_analogs = get_analogs( EXR_bo[ 8:12 ], convert_deap_list( PC_bo[ 6:8 ] ), range( 21, 25 ), tb_stat )
	print "\nFirst block, analogs:" 
	print tr_fb_analogs
	print "\nSecond block, analogs:"
	print tr_sb_analogs
	print "\nThird block, analogs:"
	print tr_tb_analogs

	print "\nFIRST + THIRD ROUNDS:"
	tot_fb_analogs = join_analogs( fr_fb_analogs, tr_fb_analogs )
	tot_sb_analogs = join_analogs( fr_sb_analogs, tr_sb_analogs )
	tot_tb_analogs = join_analogs( fr_tb_analogs, tr_tb_analogs )

	print "\nFirst block, analogs:" 
	print tot_fb_analogs
	print "\nSecond block, analogs:"
	print tot_sb_analogs
	print "\nThird block, analogs:"
	print tot_tb_analogs

	return tot_fb_analogs, tot_sb_analogs, tot_tb_analogs

def main():
	print "This module hasn't main call!"
	return

if __name__ == "__main__":
	sys.exit( main() )
