# coding: utf8

__author__ = "rockosov@gmail.com"

import sys

import blocks
import bits_ops
import config as cfg

def generate_keys( key ):
	k1 = bits_ops.get_bits( key, cfg.EXT_HALF_BLOCK_SIZE, cfg.EXT_HALF_BLOCK_SIZE )
	k2 = bits_ops.get_bits( key, cfg.EXT_HALF_BLOCK_SIZE / 2, cfg.EXT_HALF_BLOCK_SIZE )
	k3 = bits_ops.get_bits( key, 0, cfg.EXT_HALF_BLOCK_SIZE )
	return k1, k2, k3

def F( input, key ):
	f_block = blocks.Block( 1 )
	s_block = blocks.Block( 2 )
	t_block = blocks.Block( 3 )
	E_perm = blocks.Permutation( "E" )
	P_perm = blocks.Permutation( "P" )

	input = E_perm.make_permutation( input, 1 )
	input ^= key
	a1 = bits_ops.get_bits( input, 8, 4 )
	a2 = bits_ops.get_bits( input, 4, 4 )
	a3 = bits_ops.get_bits( input, 0, 4 )

	c1 = f_block.substitution( a1 )
	c2 = s_block.substitution( a2 )
	c3 = t_block.substitution( a3 )

	c = ( c1 << 5 ) | ( c2 << 2 ) | ( c3 )

	out = P_perm.make_permutation( c, 1 )

	return out

def encrypt( plain_text, key ):
	XR = bits_ops.get_bits( plain_text, 0, cfg.HALF_BLOCK_SIZE )
	XL = bits_ops.get_bits( plain_text, cfg.HALF_BLOCK_SIZE, cfg.HALF_BLOCK_SIZE )

	keys = generate_keys( key )

	for round_num in range( 3 ):
		cur_key = keys[ round_num ]
		out = F( XR, cur_key )
		XL ^= out
		if round_num != 2:
			temp = XL
			XL = XR
			XR = temp
	result = ( XL << cfg.HALF_BLOCK_SIZE ) | XR
	return result

def decrypt( cipher_text, key ):
	YR = bits_ops.get_bits( cipher_text, 0, cfg.HALF_BLOCK_SIZE )
	YL = bits_ops.get_bits( cipher_text, cfg.HALF_BLOCK_SIZE, cfg.HALF_BLOCK_SIZE )

	keys = generate_keys( key )

	for round_num in range( 3 )[ ::-1 ]:
		cur_key = keys[ ( round_num ) ]
		out = F( YR, cur_key )
		YL ^= out
		if round_num != 0:
			temp = YL
			YL = YR
			YR = temp
	result = ( YL << cfg.HALF_BLOCK_SIZE ) | YR
	return result

def test():	
	plain_text = 55203
	key = 1760619
	print "plain_text:", plain_text
	cipher_text = encrypt( plain_text, key ) 
	print "cipher_text:", cipher_text
	print "plain_text( after decrypt ):", decrypt( cipher_text, key )
	return

def main():
	test()
	return

if __name__ == "__main__":
	sys.exit( main() )
