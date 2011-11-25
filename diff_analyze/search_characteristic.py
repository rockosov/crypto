import sys
from blocks import *

__author__ = "rockosov@gmail.com"

def main():
	
	f_block = Block( 1 )
	s_block = Block( 2 ) 
	t_block = Block( 3 )

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

	print "Buid and print diff_table:"
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
	result = 12
	print bin( result )
	result = E_perm.make_permutation( result, 1 )
	print bin( result )
	result = E_perm.make_permutation( result, -1 )
	print bin( result )
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
	print variants
	print search_valid_bits( variants, E_perm.inverse )

if __name__ == "__main__":
	sys.exit(main())
