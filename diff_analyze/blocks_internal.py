# coding: utf8

from sys import stdout, path

path.append( "../" )

import config as conf
import bits_ops
import blocks

__author__ = "rockosov@gmail.com"

##
# @brief описывает блоки замены и методы работы с ними 
class Block_Internal ( blocks.Block ):
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

		# значение функции блоков на множестве определения [0;15]
		self.a_output = []
		for i in range( 16 ):
			self.a_output.append( self.substitution( i ) )

		self.diff_table = []
		return

	##
	# @brief печатает таблицу вероятностей появления дифференциала C от дифференциала A
	#
	# @return
	#	@retval ValueError - если таблица пуста
	def print_diff_table( self ):
		if self.diff_table == []:
			raise ValueError, "diff_table is empty!"
		print "diff_table of block %d:" % self.num
		for i in self.diff_table:
			for j in i:
				print "%02d" % j ,
			print
		return
	
	##
	# @brief строит таблицу вероятностей появления dС от dA
	#
	def build_diff_table( self ):
		# подготовим место
		self.diff_table.extend( range( 16 ) )
		for i in range( len( self.diff_table ) ):
			self.diff_table[ i ] = range( 16 )
			for j in range( len( self.diff_table[ i ] ) ):
				# и инициализируем как нужно
				self.diff_table[ i ][ j ] = 0
		for delta_a in range( 16 ):
			for a1 in range( 16 ):
				a2 = delta_a ^ a1
				# посчитаем c1 и c2
				c1 = self.substitution( a1 )
				c2 = self.substitution( a2 )
				# вычислим delta_c
				delta_c = c1 ^ c2
				# запомним
				self.diff_table[delta_a][delta_c] += 1
		return

	##
	# @brief ищет максимальные значения вероятности
	#
	# @return результат работы
	#	@retval out - представляет собой список вида [[x11, x21, x31], ..., [x1n, x2n, x3n]],
	#			где x1i = dA, x2i = dC, x3i = maximum
	#	@retval ValueError - если таблица пуста
	def max_in_diff_table( self ):
		result = list()
		if self.diff_table == []:
			raise ValueError, "diff_table is empty!"
		for i in self.diff_table[1:]:
			maximum = max( i )
			for j in range( len( i ) ):
				if maximum == i[ j ]:
					result.append( ( self.diff_table.index( i ), j, i[ j ] ) )
		temp = max( result, key = lambda current: current[2] )
		out = list()
		for index, value in enumerate( result ):
			if value[ 2 ] == temp[ 2 ]:
				out.append( value )
		return out

##
# @brief ищет правильные сочетания битов дифференциалов dA и dC
#
# @param variants - список, в котором содеражтся варианты диференциалов 1, 2, 3 блоков
#			в виде: [ [ варианты 1 блока ], [ варианты 2 блока ], [ варианты 3 блока ] ]
# @param rules - список правил, содержащий номера битов, какие нужно сравнивать
#
# @return список, который содержит правильные сочетания битов
def search_valid_bits( variants, rules ):
	result = list()
	first, second, third = variants
	flag = 0
	for i in first:
		for j in second:
			for k in third:
				probable = ( i[ 0 ] << 8 ) + ( j[ 0 ] << 4 ) + ( k[ 0 ] )
				for current_bits in rules:
					if len( current_bits ) > 1:
						res = bits_ops.get_bit( probable, conf.EXT_HALF_BLOCK_SIZE - current_bits[ 0 ] )
						for bit_num in current_bits:
							tmp = bits_ops.get_bit( probable, conf.EXT_HALF_BLOCK_SIZE - bit_num )
							if tmp != res:
								res = -1
						if res < 0:
							flag = 0
							break
					flag = 1
				if flag == 1:
					result.append( i )
					result.append( j )
					result.append( k )
	return result
