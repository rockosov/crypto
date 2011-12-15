# coding: utf8

from sys import stdout

import config as conf
import bits_ops

__author__ = "rockosov@gmail.com"

##
# @brief описывает блоки замены и методы работы с ними 
class Block ( object ):
	##
	# @brief конструктор
	#
	# @param num - номер блока ( 1, 2, 3 )
	def __init__( self, num ):
		if num == 1:
			self.content = conf.FIRST_BLOCK
			self.var_num = conf.FIRST_BLOCK_NUM
		elif num == 2:
			self.content = conf.SECOND_BLOCK
			self.var_num = conf.SECOND_BLOCK_NUM
		elif num == 3:
			self.content = conf.THIRD_BLOCK
			self.var_num = conf.THIRD_BLOCK_NUM
		else:
			raise ValueError, "Error of input num!"

		self.num = num

		return

	##
	# @brief печатает блок
	def print_block( self ):
		print "Blocks", self.num, "[", self.var_num, "]:"
		for i in self.content:
			for j in i:
				stdout.write(str(j) + " ")
		print

	##
	# @brief выполняет непосредственно замену
	#
	# @param bits - вход функции замены
	#
	# @return результат
	def substitution( self, bits ):
		bits &= 15 # если поступили биты, длина которых больше 4
		if self.num == 3:
			return self.content[(bits & 1) + ((bits & 8) >> 2)][(bits & 6) >> 1]
		else:
			return self.content[bits >> 3][bits & 7]

##
# @brief описывает перестановки 
class Permutation ( object ):
	##
	# @brief конструктор
	#
	# @param initial_name		[ in ] - имя перестановки ( E - Extended; P - prime )
	def __init__( self, initial_name ):
		if initial_name == "E":
			self.direct = conf.PERM_EXT
		elif initial_name == "P":
			self.direct = conf.PERM
		else:
			raise ValueError, "Unknown name of permutation"
		self.inverse = self.__inverse( self.direct )
		return

	##
	# @brief вычисляет инверсный порядок перестановки
	#
	# @param direct		[ in ] - прямой порядок
	#
	# @return непосредственно порядок
	def __inverse( self, direct):
		result = range( max( direct ) )
		for i in range( len( result ) ):
			result[i] = []
		for i in range( len( direct ) ):
			result[ direct[ i ] - 1 ].append(i + 1)
		return result

	##
	# @brief главная функция перестановки
	#
	# @param bits		[ in ] - биты для перестановки
	# @param mode		[ in ] - режим ( 1 - прямая перестановка; -1 - обратная перестановка )
	#
	# @return переставленные биты
	def make_permutation( self, bits, mode ):
		result = 0
		direct_size = len( self.direct )
		inverse_size = len( self.inverse )
		if mode == 1:
			# используем прямую перестановку
			for i in range( direct_size ):
				result = bits_ops.set_bit( result, ( direct_size - i - 1 ), bits_ops.get_bit( bits, ( inverse_size - self.direct[ i ] ) ) )
		elif mode == -1:
			# используем обратную перестановку	
			for i in range( len( self.inverse ) ):
				result = bits_ops.set_bit( result, ( inverse_size - i - 1 ), bits_ops.get_bit( bits, ( direct_size - self.inverse[ i ][ 0 ] ) ) )
		else:
			raise ValueError, "Invalid mode of permutation"
		return result
