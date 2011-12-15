# coding=utf-8

import sys

sys.path.append( "../" )

from blocks_internal import *
from blocks import Permutation
import bits_ops as bops
import config as cfg

__author__ = "rockosov@gmail.com"

##
# @brief ищет характеристику для генерации правильных текстов
#	строит блоки и заполняют всю нужную информацию о них
#
# @return экзмепляры блоков
def search():
	f_block = Block_Internal( 1 )
	s_block = Block_Internal( 2 ) 
	t_block = Block_Internal( 3 )

	print "Print substitution blocks:"
	f_block.print_block()
	s_block.print_block()
	t_block.print_block()
	print

	print "Print A dependence of substitution blocks:"
	print "a_output of 1 block:", f_block.a_output
	print "a_output of 2 block:", s_block.a_output
	print "a_output of 3 block:", t_block.a_output
	print

	print "Build and print diff_table:"
	f_block.build_diff_table()
	f_block.print_diff_table()
	s_block.build_diff_table()
	s_block.print_diff_table()
	t_block.build_diff_table()
	t_block.print_diff_table()
	print

	print "Eval and print maximum of diff_tables:"
	f_block_max = list()
	s_block_max = list()
	t_block_max = list()
	f_block_max = f_block.max_in_diff_table()
	print "First block Maximum:", f_block_max
	s_block_max = s_block.max_in_diff_table()
	print "Second block Maximum:", s_block_max
	t_block_max = t_block.max_in_diff_table()
	print "Third block Maximum:", t_block_max
	print

	print"Build permutation blocks:"
	E_perm = Permutation( "E" )
	P_perm = Permutation( "P" )
	print "E-permutation:"
	print "DIRECT"
	print E_perm.direct
	print "INVERSE"
	print E_perm.inverse
	print "P-permutation:"
	print "DIRECT"
	print P_perm.direct
	print "INVERSE"
	print P_perm.inverse
	print

	variants = list()
	variants.append( list( f_block_max ) )
	variants.append( list( s_block_max ) )
	variants.append( list( t_block_max ) )
	print "variants:", variants
	valid = search_valid_bits( variants, E_perm.inverse )
	print "valid bits:", valid
	
	if valid == []:
		print "Cant't search valid bits!"
		return -1
	dA = ( valid[ 0 ][ 0 ] << 8 ) | ( valid[ 1 ][ 0 ] << 4 ) | ( valid[ 2 ][ 0 ] )
	dC = ( valid[ 0 ][ 1 ] << 5 ) | ( valid[ 1 ][ 1 ] << 2 ) | ( valid[ 2 ][ 1 ] )
	print "dA =", bin( dA ), " dC =", bin( dC )
	dXR = E_perm.make_permutation( dA, -1 )
	dXL = P_perm.make_permutation( dC, 1 )
	print "Characteristic:"
	print "dXR ( dYR ) =", bops.full_bin( dXR, cfg.HALF_BLOCK_SIZE ), " dXL =", bops.full_bin( dXL, cfg.HALF_BLOCK_SIZE )

	return f_block, s_block, t_block, E_perm, P_perm

def main():
	search()

if __name__ == "__main__":
	sys.exit( main() )
