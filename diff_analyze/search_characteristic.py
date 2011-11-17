import sys
from blocks import Block

__author__ = "rockosov@gmail.com"

def main():
	f_block = Block( 1 )
	s_block = Block( 2 ) 
	t_block = Block( 3 )

	f_block.print_block()
	s_block.print_block()
	t_block.print_block()

	example = 10
	print f_block.substitution( example )
	print s_block.substitution( example )
	print t_block.substitution( example )

if __name__ == "__main__":
	sys.exit(main())
