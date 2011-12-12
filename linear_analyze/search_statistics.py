# coding = utf-8

__author__ = "rockosov@gmail.com"

import sys
sys.path.append( "../" )

import blocks_internal

def main():
	first_block = blocks_internal.Block_Internal( 1 )
	second_block = blocks_internal.Block_Internal( 2 )
	third_block = blocks_internal.Block_Internal( 3 )

	print "First Block:"
	first_block.print_block()
	
	print "Second Block:"
	second_block.print_block()

	print "Third Block:"
	third_block.print_block()

	print "Y of first block:"
	print first_block.Y

	print "Y of second block:"
	print second_block.Y

	print "Y of third block:"
	print third_block.Y

	print "\nStatistics of first block:"
	first_block.build_statistics()
	print first_block.statistics

	print "\nStatistics of second block:"
	second_block.build_statistics()
	print second_block.statistics

	print "\nStatistics of third block:"
	third_block.build_statistics()
	print third_block.statistics

	print first_block.get_good_stat()
	print second_block.get_good_stat()
	print third_block.get_good_stat()

if __name__ == "__main__":
	sys.exit( main() )
