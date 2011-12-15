# coding: utf8

__author__ = "rockosov@gmail.com"

import sys

import blocks
import bits_ops
import config as cfg

##
# @brief генерирует раундовые подключи
#
# @param key	[ in ] - ключ алгоритма
#
# @return кортеж из раундовых подключей
def generate_keys( key ):
	k1 = bits_ops.get_bits( key, cfg.EXT_HALF_BLOCK_SIZE, cfg.EXT_HALF_BLOCK_SIZE )
	k2 = bits_ops.get_bits( key, cfg.EXT_HALF_BLOCK_SIZE / 2, cfg.EXT_HALF_BLOCK_SIZE )
	k3 = bits_ops.get_bits( key, 0, cfg.EXT_HALF_BLOCK_SIZE )
	return k1, k2, k3

##
# @brief функция F алгоритма
#
# @param input		[ in ] - входная последовательность
# @param key		[ in ] - раундовый подключ
#
# @return выходная последовательность
def F( input, key ):
	# создаем служебные блоки
	f_block = blocks.Block( 1 )
	s_block = blocks.Block( 2 )
	t_block = blocks.Block( 3 )
	E_perm = blocks.Permutation( "E" )
	P_perm = blocks.Permutation( "P" )

	# перестановка с расширением
	input = E_perm.make_permutation( input, 1 )
	# xor с ключом
	input ^= key
	# замена
	a1 = bits_ops.get_bits( input, 8, 4 )
	a2 = bits_ops.get_bits( input, 4, 4 )
	a3 = bits_ops.get_bits( input, 0, 4 )

	c1 = f_block.substitution( a1 )
	c2 = s_block.substitution( a2 )
	c3 = t_block.substitution( a3 )

	c = ( c1 << 5 ) | ( c2 << 2 ) | ( c3 )

	# обычная перестановка
	out = P_perm.make_permutation( c, 1 )

	return out

##
# @brief зашифровывает сообщение на ключе key
#
# @param plain_text	[ in ] - открытый текст
# @param key		[ in ] - ключ
#
# @return шифр-текст
def encrypt( plain_text, key ):
	XR = bits_ops.get_bits( plain_text, 0, cfg.HALF_BLOCK_SIZE )
	XL = bits_ops.get_bits( plain_text, cfg.HALF_BLOCK_SIZE, cfg.HALF_BLOCK_SIZE )

	# генерируем раундовые подключи
	keys = generate_keys( key )

	# выполняем 3 раунда шифрования
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

##
# @brief расшифровывает сообщение на ключе key
#
# @param cipher_text	[ in ] - шифр-текст
# @param key		[ in ] - ключ
#
# @return открытый текст
def decrypt( cipher_text, key ):
	YR = bits_ops.get_bits( cipher_text, 0, cfg.HALF_BLOCK_SIZE )
	YL = bits_ops.get_bits( cipher_text, cfg.HALF_BLOCK_SIZE, cfg.HALF_BLOCK_SIZE )

	# генерируем раундовые подключи
	keys = generate_keys( key )

	# выполняем 3 раунда шифрования
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
	plain_text = 26559
	key = 1960966
	print "plain_text:", bits_ops.full_bin( plain_text, cfg.BLOCK_SIZE )
	cipher_text = encrypt( plain_text, key ) 
	print "cipher_text:", bits_ops.full_bin( cipher_text, cfg.BLOCK_SIZE )
	print "plain_text( after decrypt ):", bits_ops.full_bin( decrypt( cipher_text, key ), cfg.BLOCK_SIZE )
	return

def main():
	test()
	return

if __name__ == "__main__":
	sys.exit( main() )
